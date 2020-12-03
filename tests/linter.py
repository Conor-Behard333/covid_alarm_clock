"""Used to test the formatting of the code using pylint"""
import pylint.lint

pylint_opts = ['../logger_setup.py', '../main.py', '../api_handling/get_config_info.py', '../api_handling/get_covid_info.py',
               '../api_handling/get_news_info.py', '../api_handling/get_weather_info.py']
pylint.lint.Run(pylint_opts)
