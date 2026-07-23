"""
@author: Matthew Gotham

Functions for pricing and analyzing European-style and American-style
options, using the binomial options pricing model (specifically, the
Cox-Ross-Rubinstein model).
"""

import numpy as np
from scipy.optimize import minimize_scalar


def get_grids(price:float, strike:float, to_expiry:int, rfr:float, vol:float,
              call:bool, american:bool=False, div_yield:float=0,
              in_year:int=252) -> tuple[np.ndarray, np.ndarray]:
    """
    Produces the grids for mapping price paths and option values at various
    points.
    
    Parameters
    ----------
    price:
        The current price of the underlying.
    strike:
        The strike price of the option.
    to_expiry:
        The number of periods to expiry. Set in combination with in_year.
    rfr:
        The annualized "risk-free" interest rate.
    vol:
        The annualized expected/implied volatility of the underlying.
    call:
        True for a call option, False for a put.
    american:
        True for an American-style option, False (default) for European-
        style.
    div_yield:
        The annualized dividend yield for the underlying (default: 0)
    in_year:
        The number of periods in a year. Default: 252 (trading days).
    
    Returns
    -------
    A pair:
        binom_grid: the grid of price paths
        value_grid: the grid of option values
    """
    periods = to_expiry+1
    d_rate = np.exp(rfr/in_year)-1
    d_dividend = np.exp(div_yield/in_year)-1
    d_vol = vol/in_year**0.5
    up = np.exp(d_vol)
    down = 1/up
    p_up = (np.exp(d_rate-d_dividend)-down)/(up-down)
    p_down = 1-p_up
    #
    binom_grid = np.empty((periods,periods))
    binom_grid.fill(np.nan)
    binom_grid[0,0] = price
    #
    for col in range(1,binom_grid.shape[1]):
        for row in range(col+1):
            binom_grid[row,col] = binom_grid[row-1,col-1]/np.exp(d_vol)\
                if row==col else binom_grid[row,col-1]*np.exp(d_vol)
    #
    if call:
        value_grid = binom_grid-strike
    else:
        value_grid = strike-binom_grid
    value_grid[value_grid<0] = 0
    #
    for col in range(value_grid.shape[1]-2, -1, -1):
        for row in range(col+1):
            up_val = value_grid[row,col+1]*p_up*np.exp(-d_rate)
            down_val = value_grid[row+1,col+1]*p_down*np.exp(-d_rate)
            if american:
                value_grid[row,col] = max(value_grid[row,col],
                                             up_val+down_val)
            else:
                value_grid[row,col] = up_val+down_val
    return (binom_grid,value_grid)
    

def get_premium_greeks(price:float, strike:float, dte:int, rfr:float,
                       vol:float, call:bool, american:bool=False,
                       div_yield:float=0, days_in_year:int=252) -> dict:
    """
    Price an option based on the usual parameters, and get (some of) the
    associated Greeks.
    
    Parameters
    ----------
    price:
        The current price of the underlying.
    strike:
        The strike price of the option.
    dte:
        The number of days to expiry. Set in combination with days_in_year
        (it's up to you whether to use calendar or trading days).
    rfr:
        The annualized "risk-free" interest rate.
    vol:
        The annualized expected/implied volatility of the underlying.
    call:
        True for a call option, False for a put.
    american:
        True for an American-style option, False (default) for European-
        style.
    div_yield:
        The annualized dividend yield for the underlying (default: 0)
    days_in_year:
        Set to 365 (or 365.25?) if you want to count the days to expiry
        as calendar days, otherwise some other number (default: 252) if you
        want to use trading days.
    
    Returns
    -------
    A dict with values for Premium, Delta, Gamma, and Theta.
    """
    # Give the grids a minimum depth.
    if dte>99:
        binom_grid, value_grid = get_grids(price, strike, dte, rfr, vol, call,
                                           american, div_yield, days_in_year)
        theta = (value_grid[1,2]-value_grid[0,0])/2
    else:
        factor = round(100/dte)
        binom_grid, value_grid = get_grids(price, strike, dte*factor, rfr, vol,
                                           call, american, div_yield,
                                           days_in_year*factor)
        theta = (value_grid[1,2]-value_grid[0,0])/(2/factor)
    premium = value_grid[0,0]
    delta = (value_grid[0,1]-value_grid[1,1])/(binom_grid[0,1]
                                               -binom_grid[1,1])
    
    delta_up = (value_grid[0,2]-value_grid[1,2])/(binom_grid[0,2]
                                                  -binom_grid[1,2])
    delta_down = (value_grid[1,2]-value_grid[2,2])/(binom_grid[1,2]
                                                    -binom_grid[2,2])
    gamma = (delta_up-delta_down)/(binom_grid[0,1]-binom_grid[1,1])
    return {'Premium': premium,
            'Delta': delta,
            'Gamma': gamma,
            'Theta': theta}

def get_premium(*args, **kwargs) -> float:
    return get_premium_greeks(*args, **kwargs)['Premium']


# def get_premium(price:float, strike:float, dte:int, rfr:float, vol:float,
#                 call:bool, american:bool=False, div_yield:float=0,
#                 days_in_year:int=252) -> float:
#     """
#     Price an option based on the usual parameters, and get (some of) the
#     associated Greeks.
    
#     Parameters
#     ----------
#     price:
#         The current price of the underlying.
#     strike:
#         The strike price of the option.
#     dte:
#         The number of days to expiry. Set in combination with days_in_year
#         (it's up to you whether to use calendar or trading days).
#     rfr:
#         The annualized "risk-free" interest rate.
#     vol:
#         The annualized expected/implied volatility of the underlying.
#     call:
#         True for a call option, False for a put.
#     american:
#         True for an American-style option, False (default) for European-
#         style.
#     div_yield:
#         The annualized dividend yield for the underlying (default: 0)
#     days_in_year:
#         Set to 365 (or 365.25?) if you want to count the days to expiry
#         as calendar days, otherwise some other number (default: 252) if you
#         want to use trading days.
    
#     Returns
#     -------
#     A premium for the option in question.
#     """
#     binom_grid, value_grid = get_grids(price, strike, dte, rfr, vol, call,
#                                        american, div_yield, days_in_year)
#     return value_grid[0,0]


def get_iv(price:float, strike:float, premium:float, dte:int, rfr:float,
           call:bool, american:bool=False, div_yield:float=0,
           days_in_year:int=252) -> float:
    """
    Get the implied volatility of an option based on the usual parameters.
    
    Parameters
    ----------
    price:
        The current price of the underlying.
    strike:
        The strike price of the option.
    premium:
        The premium paid for the option.
    dte:
        The number of days to expiry. Set in combination with days_in_year
        (it's up to you whether to use calendar or trading days).
    rfr:
        The annualized "risk-free" interest rate.
    call:
        True for a call option, False for a put.
    american:
        True for an American-style option, False (default) for European-
        style.
    div_yield:
        The annualized dividend yield for the underlying (default: 0)
    days_in_year:
        Set to 365 (or 365.25?) if you want to count the days to expiry
        as calendar days, otherwise some other number (default: 252) if you
        want to use trading days.
    
    Returns
    -------
    A premium for the option in question.
    """
    def trial(x:float) -> float:
        "Getting the premium"
        result = get_premium(price, strike, dte, rfr, x, call, american,
                             div_yield, days_in_year)
        return abs(result-premium)
    res = minimize_scalar(trial, bounds=(0,1))
    return res.x


def get_vega(price:float, strike:float, dte:int, rfr:float, vol:float,
             call:bool, american:bool=False, div_yield:float=0,
             days_in_year:int=252) -> dict:
    """
    Calculates a figure for vega using numerical differentiation.
    
    Parameters
    ----------
    price:
        The current price of the underlying.
    strike:
        The strike price of the option.
    dte:
        The number of days to expiry. Set in combination with days_in_year
        (it's up to you whether to use calendar or trading days).
    rfr:
        The annualized "risk-free" interest rate.
    vol:
        The annualized expected/implied volatility of the underlying.
    call:
        True for a call option, False for a put.
    american:
        True for an American-style option, False (default) for European-
        style.
    div_yield:
        The annualized dividend yield for the underlying (default: 0)
    days_in_year:
        Set to 365 (or 365.25?) if you want to count the days to expiry
        as calendar days, otherwise some other number (default: 252) if you
        want to use trading days.
    
    Returns
    -------
    Vega in currency units per percentage point.
    """
    up_val = get_premium(price, strike, dte, rfr, vol+0.00001, call, american,
                         div_yield, days_in_year)
    down_val = get_premium(price, strike, dte, rfr, vol-0.00001, call, american,
                           div_yield, days_in_year)
    vega = (up_val-down_val)/0.002
    return vega


def get_rho(price:float, strike:float, dte:int, rfr:float, vol:float,
             call:bool, american:bool=False, div_yield:float=0,
             days_in_year:int=252) -> dict:
    """
    Calculates a figure for rho using numerical differentiation.
    
    Parameters
    ----------
    price:
        The current price of the underlying.
    strike:
        The strike price of the option.
    dte:
        The number of days to expiry. Set in combination with days_in_year
        (it's up to you whether to use calendar or trading days).
    rfr:
        The annualized "risk-free" interest rate.
    vol:
        The annualized expected/implied volatility of the underlying.
    call:
        True for a call option, False for a put.
    american:
        True for an American-style option, False (default) for European-
        style.
    div_yield:
        The annualized dividend yield for the underlying (default: 0)
    days_in_year:
        Set to 365 (or 365.25?) if you want to count the days to expiry
        as calendar days, otherwise some other number (default: 252) if you
        want to use trading days.
    
    Returns
    -------
    Rho in currency units per percentage point.
    """
    up_val = get_premium(price, strike, dte, rfr+0.00001, vol, call, american,
                         div_yield, days_in_year)
    down_val = get_premium(price, strike, dte, rfr-0.00001, vol, call, american,
                           div_yield, days_in_year)
    rho = (up_val-down_val)/0.002
    return rho
