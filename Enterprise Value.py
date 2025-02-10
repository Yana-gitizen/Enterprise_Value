#!/usr/bin/env python
# coding: utf-8

# In[31]:


# Import necessary libraries
import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display


# In[33]:


# Input widgets for DCF parameters
initial_revenue = widgets.IntSlider(
    value=10000000,  # Example initial revenue
    min=1000000,
    max=50000000,
    step=100000,
    description='Initial Revenue:'
)


# In[35]:


revenue_growth_rate = widgets.FloatSlider(value=0.05, min=-0.1, max=0.2, step=0.01, description='Revenue Growth Rate:')
ebit_margin = widgets.FloatSlider(value=0.15, min=0.0, max=0.3, step=0.01, description='EBIT Margin:')
tax_rate = widgets.FloatSlider(value=0.25, min=0.0, max=0.5, step=0.01, description='Tax Rate:')
capex_to_revenue = widgets.FloatSlider(value=0.05, min=0.0, max=0.2, step=0.01, description='CAPEX/Revenue:')
depreciation_to_revenue = widgets.FloatSlider(value=0.03, min=0.0, max=0.1, step=0.01, description='Depreciation/Revenue:')
wacc = widgets.FloatSlider(value=0.08, min=0.0, max=0.2, step=0.01, description='WACC:')
terminal_growth_rate = widgets.FloatSlider(value=0.02, min=0.0, max=0.05, step=0.01, description='Terminal Growth Rate:')
forecast_years = widgets.IntSlider(value=5, min=3, max=10, step=1, description='Forecast Years:')

calculate_button = widgets.Button(description='Calculate Enterprise Value')


# In[37]:


output = widgets.Output()


# In[43]:


# DCF calculation function
def calculate_enterprise_value(initial_revenue, revenue_growth_rate, ebit_margin, tax_rate, capex_to_revenue, depreciation_to_revenue, wacc, terminal_growth_rate, forecast_years):
    # Initial values (Year 0)
    revenue = initial_revenue
    ebit = revenue * ebit_margin
    tax = ebit * tax_rate
    nopat = ebit - tax
    capex = revenue * capex_to_revenue
    depreciation = revenue * depreciation_to_revenue
    fcf = nopat + depreciation - capex

    # Project future cash flows
    fcf_projections = []
    for year in range(1, forecast_years + 1):
        revenue *= (1 + revenue_growth_rate)
        ebit = revenue * ebit_margin
        tax = ebit * tax_rate
        nopat = ebit - tax
        capex = revenue * capex_to_revenue
        depreciation = revenue * depreciation_to_revenue
        fcf = nopat + depreciation - capex
        fcf_projections.append(fcf)

    # Calculate terminal value
    terminal_value = fcf * (1 + terminal_growth_rate) / (wacc - terminal_growth_rate)  # Gordon Growth Model

    # Discount future cash flows
    pv_fcf = [fcf / (1 + wacc)**i for i, fcf in enumerate(fcf_projections, start=1)]
    pv_terminal_value = terminal_value / (1 + wacc)**forecast_years

    # Calculate enterprise value
    enterprise_value = sum(pv_fcf) + pv_terminal_value

    return enterprise_value

# Button click event handler
def on_calculate_button_clicked(b):
    with output:
        output.clear_output()
        enterprise_value = calculate_enterprise_value(
            initial_revenue.value,
            revenue_growth_rate.value,
            ebit_margin.value,
            tax_rate.value,
            capex_to_revenue.value,
            depreciation_to_revenue.value,
            wacc.value,
            terminal_growth_rate.value,
            forecast_years.value
        )
        print(f'Enterprise Value: ${enterprise_value:,.2f}')

calculate_button.on_click(on_calculate_button_clicked)


# In[ ]:


# Display the widgets and output
display(initial_revenue, revenue_growth_rate, ebit_margin, tax_rate, capex_to_revenue, depreciation_to_revenue, wacc, terminal_growth_rate, forecast_years, calculate_button, output)

