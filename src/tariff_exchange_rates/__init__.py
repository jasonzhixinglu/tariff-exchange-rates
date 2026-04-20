from .economy    import compute_allocation
from .equilibrium import solve_2country, solve_3country
from .tariffs    import (make_tariff_matrix, free_trade, uniform_tariff,
                         isolated_tariff, trade_war)
from .parameters import (make_params_2country, make_params_3country,
                         CALIBRATIONS, TARIFF_REGIMES)
from .plotting   import (plot_tb_locus, plot_equilibria,
                         plot_calibration_results)
