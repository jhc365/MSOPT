---
title: "Artifacts"
output:
  html_document:
    toc: yes
pagetitle: Artifacts
---

All scripts can be found in `/home/user/Documents/xyntia_benchmarks/`.

# Usage

## Synthesizing expressions from sampling files

To synthesize an expression from a sampling file, execute the following command:

```{#mycode .bash .numberLines}
./xyntia.sh [-opset <opset>] [-time <time>] [-heur <heur>] <file>
```

where:

* *opset* is the set of operators considered among `mba`, `expr`, `full` (default expr). Other sets of operators are available (`mbaite`, `mbashift`) but they are specific to some experiments (see below);
* *time* is the time budget of the synthesis in seconds (default: 60s);
* *heur* is the abbreviation for the search heuristic to be used (see below) and defaults to *ils*;
* *file* is the sampling file containing observed I/O behaviors. See the section **Sampling** to generate one.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">heuristic</th>
<th scope="col" class="org-left">abbreviation</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">Iterated Local Search</td>
<td class="org-left">ils</td>
</tr>


<tr>
<td class="org-left">Hill Climbing</td>
<td class="org-left">hc</td>
</tr>


<tr>
<td class="org-left">Random Walk</td>
<td class="org-left">rw</td>
</tr>


<tr>
<td class="org-left">Simulated Annealing</td>
<td class="org-left">sa</td>
</tr>


<tr>
<td class="org-left">Metropolis-Hastings</td>
<td class="org-left">mh</td>
</tr>
</tbody>
</table>




## Sampling

To generate a sampling file for a given expression, execute:
```{#mycode .bash .numberLines}
python3 ./sample.py --expr "<expr>" > output.json
```
Note that *\<expr\>* must be a python expression. Moreover, variables must be named v0, v1, v2 and so on up to v5. Here is an example:

```{#mycode .bash .numberLines}
python3 ./sample.py --expr "v0 + v1" > output.json
```


## Replaying Xyntia benchmarks

The script bench.py is given to replay the experiments over the different datasets. If the `--fast` option is setted, bench.py will not check results with Z3. Thus, only the success rate and mean quality will be computed (not the equivalence range). It enables to save time.

To replay results from Figure 5 : 

```{#mycode .bash .numberLines}
timeout = 1 # choose your timeout

python3 ./sample.py --bench ./datasets/b2
python3 ./bench.py --bench ./datasets/b2 --opset expr --timeout $timeout
```

To replay results from Figure 8:

```{#mycode .bash .numberLines}
bp="bp1" # choose the dataset among bp1, bp2 and bp3
timeout = 60 # choose your timeout

python3 ./sample.py --bench ./datasets/$bp
python3 ./bench.py --bench ./datasets/$bp --opset expr --timeout $timeout
```

In section 8, we propose to merge handlers through *if-then-else* constructs. Thus, we distingish 4 scenarios:

* *Utopian* where Xyntia infers expressions on the perfect grammar (MBA-ITE) and samples inputs uniformly accross branches;
* *MBA-ITE* where Xyntia infers expressions on the perfect grammar (MBA-ITE) but does not sample inputs uniformly accross branches;
* *MBA-SHIFT* where Xyntia infers expressions on the MBA-Shift grammar (which is expressive enough to handle *if-then-else* construct) and does not sample inputs uniformly accross branches;
* *Default* where Xyntia is launched in default mode.

Recall that in all the scenario, we consider that the grammar contains interesting constants.

To replay results according to the different scenarios as in Figure 10:

```{#mycode .bash .numberLines}
merged="merged1" # choose the dataset among merged1, merged2, merged3, merged4, merged5
timeout = 60 # choose your timeout

## Utopian
python3 ./sample.py --bench ./datasets/$merged --ite
python3 ./bench.py --bench ./datasets/$merged --opset mbaite --timeout $timeout --utopconsts

## MBA-ITE
python3 ./sample.py --bench ./datasets/$merged
python3 ./bench.py --bench ./datasets/$merged --opset mbaite --timeout $timeout --utopconsts

## MBA-SHIFT
python3 ./sample.py --bench ./datasets/$merged
python3 ./bench.py --bench ./datasets/$merged --opset mbashift --timeout $timeout --utopconsts

## Default
python3 ./sample.py --bench ./datasets/$merged
python3 ./bench.py --bench ./datasets/$merged --opset expr --timeout $timeout --utopconsts
```
