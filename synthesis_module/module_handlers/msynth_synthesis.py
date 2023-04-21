from msynth import Synthesizer
from synthesis_module.module_handlers.HandlerBase import HandlerBase
# from synthesis_module.module_handlers.HandlerBase_VMoption import HandlerBase
import time
from miasm.expression.expression import ExprSlice

class Msynth_synth(HandlerBase):
    def __init__(self):
        self.simplifier = Synthesizer()

    def simplify_restart_ruby(self, expr, fixed_timeout=0):
        # synthesized, score = self.simplifier.synthesize_from_expression(expr,num_samples = 10)

        # timeoutlist = [2.5 for _ in range(10)]
        ruby_list = [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 1, 1,
                    2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 32, 1, 1, 2,
                    1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 1, 1, 2, 1, 1,
                    2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16, 32, 64]
        timeoutlist = [3.0, 60.0, 30.0, 10.0, 5.0, 5.0]
        score_list = [-1, -1, -1]
        time_list = [-1, -1, -1]
        try_count = -1
        count = 0

        # while(count<3):
        start = time.time()
        # for to in range(1):
        print(fixed_timeout)
        while time.time() - start < fixed_timeout:
            start_time_each = time.time()
            timeout = ruby_list[count]
            # timeout = 1
            count = count + 1
            # if fixed_timeout != 0:
            #     timeout = fixed_timeout
            # print(timeout)
            synthesized, score = self.simplifier.synthesize_from_expression_parallel(expr, num_samples=10,
                                                                                     timeout=timeout)
            print("FT = %d, T = %d" % (fixed_timeout, timeout))
            if score == 0.0:
                # return synthesized, True
                if self.semantically_equal(expr, synthesized):
                    # return synthesized, True, [score_list,time_list,try_count]
                    return synthesized, True, count

        return False, False, count


    def simplify_with_score_ruby_heuristic(self, expr, fixed_timeout=0, score_bl=0):
        # synthesized, score = self.simplifier.synthesize_from_expression(expr,num_samples = 10)
        # fixed_timeout = 60.0
        # timeoutlist = [2.5 for _ in range(10)]
        ruby_list = [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,64]
        timeoutlist = [1.0,3.0,60.0, 60.0, 30.0, 10.0, 5.0, 5.0]
        # timeoutlist = [3.0, 60.0, 30.0, 10.0, 5.0, 5.0]
        score_list = [-1, -1, -1]
        time_list = [-1, -1, -1]
        try_count = -1
        count = 0

        fixed_timeout_list = [20,30, 40,50, 60]
        ft_count = 0
        fixed_timeout = fixed_timeout_list[ft_count]

        # while(count<3):
        start = time.time()
        # for to in range(fixed_timeout):
        while time.time()-start < fixed_timeout :
            # timeout = timeoutlist[count]
            timeout = ruby_list[count]
            fixed_timeout = fixed_timeout_list[ft_count]


            synthesized, score = self.simplifier.synthesize_from_expression_parallel(expr, num_samples = 10, timeout=timeout)

            # synthesized, score = self.simplifier.synthesize_from_expression(expr, num_samples=10, timeout=timeout)
            # print(f"score : {score}      new timeout : {timeout} ")
            print(f"FT = {fixed_timeout}, T = {timeout}, score = {score}")

            if score == 0.0:
                # return synthesized, True
                if self.semantically_equal(expr, synthesized):
                    # return synthesized, True, [score_list,time_list,try_count]
                    return synthesized, True, count
                    # return synthesized, True

            if score < score_bl :
                ft_count += 1
                if ft_count == len(fixed_timeout_list):
                    ft_count = len(fixed_timeout_list)-1
            count = count + 1
        # return False, False
        return False, False, count

    def simplify(self, expr,fixed_timeout=0): # default (for PLASynth, not restart_result strategy)
        # synthesized, score = self.simplifier.synthesize_from_expression(expr,num_samples = 10)
        # fixed_timeout = 60.0
        # timeoutlist = [2.5 for _ in range(10)]
        ils_list = [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, 16,32,64]
        timeoutlist = [1.0,3.0,60.0, 60.0, 30.0, 10.0, 5.0, 5.0]
        # timeoutlist = [3.0, 60.0, 30.0, 10.0, 5.0, 5.0]
        score_list = [-1, -1, -1]
        time_list = [-1, -1, -1]
        try_count = -1
        count = 0

        fixed_timeout_list = [20, 40, 60]
        fixed_timeout_list = [20]
        ft_count = 0
        fixed_timeout = fixed_timeout_list[ft_count]

        # while(count<3):
        start = time.time()
        iter_count = 0
        for to in range(fixed_timeout):
        # while time.time()-start < timeout :
            iter_count = to+1
            # timeout = timeoutlist[count]
            timeout = 1
            fixed_timeout = fixed_timeout_list[ft_count]
            print("FT = %d, T = %d" % (fixed_timeout, timeout))
            synthesized, score = self.simplifier.synthesize_from_expression_parallel(expr, num_samples = 10, timeout=timeout)
            #if expr.is_slice():
                #synthesized = ExprSlice(synthesized,31,32)
            synthesized, score = self.simplifier.synthesize_from_expression(expr, num_samples=10, timeout=timeout)
            print(f"score : {score}      new timeout : {timeout} ")


            # score_list[to] = score
            # time_list[to] = end_time_each
            # try_count = to+1



            if score == 0.0:
                # return synthesized, True
                if self.semantically_equal(expr, synthesized):
                    # return synthesized, True, [score_list,time_list,try_count]
                    return synthesized, True

            # if score < 20 :
            #     timeout = timeoutlist[count]
            #     count = count+1
            count = count + 1
        return False, False

    def simplify_try2(self, expr,timeout = 1):
        # synthesized, score = self.simplifier.synthesize_from_expression(expr,num_samples = 10)
        timeout = 1.0
        timeoutlist = [3.0, 6.0, 7.0, 10.0, 5.0, 5.0]

        # while(count<3):
        for to in range(2):
            synthesized, score = self.simplifier.synthesize_from_expression_parallel(expr, num_samples = 10, timeout=timeout)
            # synthesized, score = self.simplifier.synthesize_from_expression(expr, num_samples=10, timeout=timeout)
            print(f"score : {score}      new timeout : {timeout} ")

            if score == 0.0:
                if self.semantically_equal(expr, synthesized):
                    # return synthesized, True, [score_list,time_list,try_count]
                    return synthesized, True

        return False, False




    def get_module_name(self):
        return "msynth-synth"