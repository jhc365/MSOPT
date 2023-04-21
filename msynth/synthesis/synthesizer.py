import logging
import multiprocessing
import time
from typing import Any, Dict, Tuple

from miasm.expression.expression import Expr
from msynth.synthesis.grammar import Grammar
from msynth.synthesis.mutations import Mutator
from msynth.synthesis.oracle import SynthesisOracle
from msynth.synthesis.state import SynthesisState
from msynth.utils.expr_utils import get_unique_variables
from msynth.utils.parallelizer import Parallelizer
from msynth.utils.unification import gen_unification_dict, reverse_unification
from miasm.expression.simplifications import expr_simp

logger = logging.getLogger("msynth.synthesizer")
import sys
from z3 import Solver,unsat
from miasm.ir.translators.z3_ir import TranslatorZ3

solver = Solver()
translator_z3 = TranslatorZ3()

class Synthesizer:
    """
    Expression synthesis based on input-output (I/O) samples.

    Based on a number of I/O samples (provided via a synthesis oracle),
    it tries to stochastically learn an expression with the same I/O behavior.
    For this, it considers program synthesis as a stochastic optimization problem:
    It randomly mutates a synthesis state (expression), measures the differences in
    the output behavior between the synthesis state and the oracle output
    using a distance function. The goal is to minimize the distance until the
    I/O behavior is the same.

    The synthesizer makes use of a grammar to generate random expressions. To mutate
    expressions, it uses a mutator that applies small changes to the synthesis state.

    The approach is inspired by:

    "Syntia: Synthesizing the Semantics of Obfuscated Code" by
    Tim Blazytko, Moritz Contag, Cornelius Aschermann and Thorsten Holz (USENIX Security 2017).
    Link: https://synthesis.to/papers/usenix17-syntia.pdf

    "Search-Based Local Blackbox Deobfuscation: Understand, Improve and Mitigate" by
    Grégoire Menguy, Sébastien Bardin, Richard Bonichon and Cauim de Souza de Lima (CCS 2021).
    Link: https://binsec.github.io/assets/publications/papers/2021-ccs.pdf

    The synthesizer provides the functionality to synthesize an expression based on a 
    given (complex) expression that represents a mathematical function f(x0, ..., xi) 
    with i inputs. Based on this expression, synthesis oracle, grammar and mutator
    will be automatically initialized. The synthesis can also be processed in parallel.
    """

    def synthesize_from_expression(self, expr: Expr, num_samples: int, timeout:float) -> Tuple[Expr, float]:
        """
        Synthesizes an expression from a given expression that represents a function f(x0, ..., xi).

        The function constructs a synthesis oracle, a grammar and a mutator. Afterward, it
        performs the stochastic search. To deal with memory, memory accesses are replaced with
        variable accesses and re-applied afterward to the synthesized expression.

        Example:

        The given expression @64[rax] + rbx - rbx is unified to p0 + p1 - p1. A synthesized
        expression p0 with he same I/O behavior is p0. After re-applying the initial variables,
        we return @64[rax].

        Args:
            expr (Expr): Expression representing a function f(x0, ..., xi) in Miasm IR.
            num_samples (int): Number of I/O samples for the synthesis oracle.

        Returns:
            Tuple[Expr, float]: Synthesized expression and its corresponding score.
        """
        # unify expression (to remove memory etc.)
        unification_dict = gen_unification_dict(expr)
        expr = expr.replace_expr(unification_dict)

        # get list of unique variables
        variables = get_unique_variables(expr)

        # generate synthesis oracle
        oracle = SynthesisOracle.gen_from_expression(
            expr, variables, num_samples)

        # init grammar
        grammar = Grammar(expr.size, variables)

        # build mutator
        mutator = Mutator.gen_from_expression(expr, grammar)

        # perform stochastic search
        state, score = self.iterated_local_search(mutator, oracle,timeout=timeout,expr=expr)

        # reverse unification and re-apply original variables
        expr = reverse_unification(
            state.get_expr_simplified(), unification_dict)

        # upcast expression if necessary
        if grammar.size > expr.size:
            expr = expr.zeroExtend(grammar.size)

        return expr, score

    def synthesize_from_expression_parallel(self, expr: Expr, num_samples: int, timeout:float) -> Tuple[Expr, float]:
        """
        Performs the synthesis for a given expression that represents a function f(x0, ..., xi) in parallel.

        The function call to `synthesize_from_expression` is parallelized. All synthesis tasks
        are clustered into the same task group and passed to a Parallelizer. If the first worker from
        the task group succeeds, other instances will be terminated. In case no worker succeeds,
        the initial provided expression will be returned.

        Args:
            expr (Expr): Expression representing a function f(x0, ..., xi) in Miasm IR.
            num_samples (int): Number of I/O samples for the synthesis oracle.

        Returns:
            Tuple[Expr, float]:  Synthesized expression and its corresponding score.
        """

        # parallelization wrapper
        # score_list = []
        # expr = expr_simp(expr)
        # # if expr.length() < 10:
        # #     return expr, 0.0
        # # if expr.is_int():
        # #     return expr, 0.0
        # if expr.length() <= 20:
        #     return expr, 0.0
        def synthesize_from_expression(results: Any, index: Any, score_list) -> None:
            result = self.synthesize_from_expression(expr, num_samples,timeout)
            # if synthesis succeeded
            score_list.append(result[1])
            # print(score_list)
            # print(result[1])
            if result[1] == 0.0:
                results[index] = result

        # prepare parallelization
        tasks = []
        task_group = f"{expr}"
        for _ in range(multiprocessing.cpu_count()):
            tasks.append((synthesize_from_expression, task_group))

        # execute in parallel
        parallelizer = Parallelizer(tasks)
        parallelizer.execute()

        # get task group result
        if task_group in parallelizer.task_group_results:
            result = parallelizer.task_group_results[task_group]
            # check if result found
            if result != None:
                return result[0], result[1]

        # print(parallelizer.min_score)
        return expr, parallelizer.min_score
        # return expr, float("inf")

    def simplify(self, expr: Expr, num_samples: int = 10) -> Expr:
        """
        Simplifies an expression via stochastic program synthesis.

        If the synthesis was not successful, the initial expression
        is returned.

        Args:
            expr (Expr): Expression to simplify in Miasm IR.
            num_samples (int, optional): Number of I/O samples for the synthesis oracle. Defaults to 10.

        Returns:
            Expr: Simplified Expression in Miasm IR.
        """
        # synthesize
        synthesized, score = self.synthesize_from_expression(
            expr, num_samples)
        # check if perfect score
        if score == 0.0:
            return synthesized

        return expr

    def semantically_equal(self, f1, f2):
        if not f2:
            return False
        solver.reset()
        # set solver timeout (Z3 expects timeout in ms)
        solver.set("timeout", 1000)
        # add contraints
        solver.add(translator_z3.from_expr(
            f1) != translator_z3.from_expr(f2))
        return solver.check() == unsat

    def iterated_local_search(self, mutator: Mutator, oracle: SynthesisOracle, timeout: int = 60,expr=None) -> Tuple[SynthesisState, float]:
        """
        Performs an iterative local search (ILS) to synthesize an expression for a given synthesis oracle.

        The algorithm tries to find a synthesis state that minimizes the distance function. Starting with an AST
        representing a single leaf, it iteratively switches between perturbation and side search. The perturbation
        mutates the best state (found so far) by replacing a subexpression with a leaf node. Afterward, it tries 
        to find better synthesis states in the side search by applying more aggressive mutations. The mutated state is
        discarded, unless it is better than the current state. If the side search does not find a better state
        (with a lower score) within 100 iterations, the algorithm continues with perturbation.

        The algorithm terminates and returns the best state and score if

        (1) the synthesis state's score is 0 (synthesis state and oracle have the same I/O behavior) or
        (2) the provided timeout is reached.

        The implementation is adapted from:

        "Search-Based Local Blackbox Deobfuscation: Understand, Improve and Mitigate" by
        Grégoire Menguy, Sébastien Bardin, Richard Bonichon and Cauim de Souza de Lima (CCS 2021).
        Link: https://binsec.github.io/assets/publications/papers/2021-ccs.pdf

        Args:
            mutator (Mutator): Mutator to mutate synthesis states.
            oracle (SynthesisOracle): Input-output oracle.
            timeout (int, optional): Timeout for synthesis. Defaults to 60.

        Returns:
            Tuple[SynthesisState, float]: Best synthesis state and its score.
        """
        # init states
        current_state = SynthesisState(
            *mutator.grammar.gen_terminal_for_state())
        current_score = float("inf")

        best_state = current_state.clone()
        best_score = float("inf")

        # init iterations and time
        iteration = 0
        start_time = time.time()

        threshold_score = 20
        mutate_count = 5

        ils_list = [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,64]
        ils_size = len(ils_list)
        short_timeout = ils_list[0]
        # start ILS
        while time.time() - start_time < timeout:
            # perturbation
            current_state = mutator.replace_subexpression_with_leaf(
                current_state)

            # side search
            change_counter = 0
            ils_timeout = ils_list[change_counter%ils_size]
            while change_counter < 100 and time.time() - start_time < timeout:
                iteration += 1
                # print(ils_timeout)
                # mutate and score
                proposed_state = mutator.mutate(current_state)
                
                # << msynth-simp로 같은지 확인 (original-proposed_state) -> if simp ? proposed = simp : continue
                proposed_score = proposed_state.get_hamming_score(
                    oracle, mutator.grammar.variables)

                # if proposed_score == 0.0:
                #     # return proposed_state, proposed_score
                #     if self.semantically_equal(proposed_state.expr_ast.replace_expr(proposed_state.replacements), expr):
                #         return proposed_state, proposed_score
                #     else:
                #         proposed_score = 21

                # the proposed state is better
                if proposed_score < current_score:
                    # reset counter
                    change_counter = 0

                    # update current state
                    current_state = proposed_state.clone()
                    current_score = proposed_score

                    if current_score < threshold_score:
                        print("# update mutate count")
                        mutate_count = 1
                    # update best state
                    if proposed_score < best_score:
                        best_state = proposed_state.clone()
                        best_score = proposed_score
                        logger.info(
                            f"best state: {best_state.get_expr()} (score: {best_score}) (iteration: {iteration})"
                        )

                    # return if perfect result found
                    # if best_score == 0.0:
                    if best_score == 0.0:
                        return best_state, best_score
                        # if self.semantically_equal(best_state.expr_ast.replace_expr(best_state.replacements), expr):
                        #     return best_state, best_score
                        # else:
                        #     current_state = SynthesisState(
                        #         *mutator.grammar.gen_terminal_for_state())
                        #     current_score = float("inf")
                        #
                        #     best_state = current_state.clone()
                        #     best_score = float("inf")

                # update change counter
                change_counter += 1
                ils_timeout = ils_list[change_counter%ils_size]

            # use best state for perturbation
            current_state = best_state.clone()

        return best_state, float("inf")
