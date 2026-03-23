# MCAmbulance
MCAmbulance is a small python package to correct Monte-Carlo samples of $B \rightarrow D_0^\ast \ell \nu$ and $B \rightarrow D_1\prime \ell \nu$ decays produced by the [basf2](https://github.com/belle2/basf2) version of [EvtGen](https://evtgen.hepforge.org) for missing phase-space factors.

MCAmbulance relies on
- numpy
- scipy

The missing phase-space factors and the reweighting strategy are described in detail in the preprint [arXiv:2602.18378](https://arxiv.org/abs/2602.18378).
MCAmbulance supports the following decays:
- $B \rightarrow D_0^\ast(\rightarrow D \pi) \ell \nu$
- $B \rightarrow D_0^\ast(\rightarrow D \eta) \ell \nu$
- $B \rightarrow D_0^\ast(\rightarrow D \pi \pi) \ell \nu$ (Note, this decay violates parity)
- $B \rightarrow D_0^\ast(\rightarrow D^\ast \pi \pi) \ell \nu$
- $B \rightarrow D_1\prime(\rightarrow D^\ast \pi) \ell \nu$
- $B \rightarrow D_1\prime(\rightarrow D^\ast \eta) \ell \nu$
- $B \rightarrow D_1\prime(\rightarrow D \pi \pi) \ell \nu$
- $B \rightarrow D_1\prime(\rightarrow D^\ast \pi \pi) \ell \nu$

# Usage
Simply include the ```mcambulance``` folder in your ```PYTHONPATH```.

Correcting $B^\pm \rightarrow D_0^\ast(\rightarrow D \pi) \mu \nu_\mu$ samples is achieved through:
```
from mcambulance import MCAmbulance

d0_d_pi_fix = MCAmbulance('bp', 'd0_d_pi', 'mu')

d0_d_pi_fix.CorrectionWeight(dpi_invM)
```

Here, ```dpi_invM``` is a numpy array containing the $D\pi$ invariant mass for each affected event.

The constructor of ```MCAmbulance``` takes three arguments:
- ```bmeson```: ```bp``` or ```b0``` for charged or neutral $B$ mesons, respectively
- ```channel```: ```d0_d_pi```, ```d0_d_eta```, ```d0_d_pipi```, ```d0_dstar_pipi```, ```d1p_dstar_pi```, ...
- ```lepton```: ```e```, ```mu``` or ```tau```


# References
If you use MCAmbulance, you should cite the following references:
- MCAmbulance: Florian Herren and Raynette van Tonder, [arXiv:2602.18378](https://arxiv.org/abs/2602.18378)
- EvtGen: David J. Lange, [Nucl.Instrum.Meth.A 462 (2001) 152-155](https://doi.org/10.1016/S0168-9002(01)00089-4)
- basf2: Belle-II Framework Software Group, [Comput.Softw.Big Sci. 3 (2019) 1, 1](https://doi.org/10.1007/s41781-018-0017-9)
- LLSW parametrisation: Adam K. Leibovich, Zoltan Ligeti, Ian M. Stewart and Mark B. Wise, [Phys.Rev.Lett. 78 (1997) 3995-3998](https://doi.org/10.1103/PhysRevLett.78.3995) & [Phys.Rev.D 57 (1998) 308-330](https://doi.org/10.1103/PhysRevD.57.308)
- Default form factor values: Florian U. Bernlochner and Zoltan Ligeti, [Phys.Rev.D 95 (2017) 1, 014022](https://doi.org/10.1103/PhysRevD.95.014022)

# Authors
 * Florian Herren <florian.s.herren@gmail.com>
 * Raynette van Tonder <raynette.vantonder@kit.edu>
