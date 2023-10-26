import io
import zipfile
import os
import requests
from typing import Callable
import pandas as pd
import numpy as np


df_state_abbr: pd.DataFrame | None = pd.read_csv(os.path.join(os.getcwd(), './data_viewer/states-abbr.csv'))


class _HeadStartLocation:

    __cache:pd.DataFrame | None = None

    @staticmethod
    def get_data() -> pd.DataFrame:
        if _HeadStartLocation.__cache is None:
            _HeadStartLocation._get_data()
        return _HeadStartLocation.__cache
    
    @staticmethod
    def _get_data():
        _HeadStartLocation.__cache =pd.read_csv('https://eclkc.ohs.acf.hhs.gov/sites/default/files/locatordata/ALL_all.csv')

    @staticmethod
    def clear_cache():
        _HeadStartLocation.__cache = None


class _HeadStartFiscal:

    __cache:dict[int, pd.DataFrame | None] = {}

    @staticmethod
    def get_data(year: int) -> pd.DataFrame:
        if _HeadStartFiscal.__cache.get(year, None) is None:
            _HeadStartFiscal._get_data(year)
        return _HeadStartFiscal.__cache[year]
    
    @staticmethod
    def _get_data(year:int):
        try:
            df = pd.read_html(f'https://eclkc.ohs.acf.hhs.gov/about-us/article/head-start-program-facts-fiscal-year-{year}')
            df =  df[1].iloc[2:, :3]
            df.columns = ['state_name', 'federal_funding', 'enroll_count', ]
            df = pd.merge(df, df_state_abbr, left_on='state_name', right_on='State', how='left').drop('State', axis=1)
            df.columns = ['state_name', 'federal_funding', 'enroll_count', 'state' ]
            df.federal_funding = df.federal_funding.map(lambda s: s.replace('$', '').replace(',', '')).astype(float)
            df.enroll_count = df.enroll_count.astype(int)
            df = df[df.state != 'US']
        except Exception as e:
            print(e)
            df = None   
        finally:
            _HeadStartFiscal.__cache[year] = df

    @staticmethod
    def clear_cache():
        _HeadStartFiscal.__cache = {}


class _SAIPE:

    __cache:dict[int, pd.DataFrame | None] = {}

    @staticmethod
    def get_data(year: int) -> pd.DataFrame:
        if _SAIPE.__cache.get(year, None) is None:
            _SAIPE._get_data(year)
        return _SAIPE.__cache[year]
    
    @staticmethod
    def _get_data(year: int) -> pd.DataFrame:
        try:
            last2 = str(year)[-2:]
            df_base = pd.read_excel(f'https://www2.census.gov/programs-surveys/saipe/datasets/{year}/{year}-state-and-county/est{last2}all.xls').drop(index=[0, 1])
            state_names = df_state_abbr.State.tolist()
            filter_out = state_names + ['United States']
            df_base = df_base[~df_base['Unnamed: 3'].isin(filter_out)]

            def to_int(v):
                try:
                    return int(v)
                except Exception as e:
                    print(e, v)
                    return 0
        
            teen_poverty = df_base.iloc[1:, 10].map(to_int)
            young_poverty = df_base.iloc[1:, 16].map(to_int)
            child_poverty = teen_poverty - young_poverty
            df = pd.DataFrame({
                'state': df_base.iloc[1:, 2],
                'county': df_base.iloc[1:, 3],
                'county_fips': df_base.iloc[1:, 0],
                'child_poverty_count': child_poverty.values, 
            })
            df[df.county.str.contains('County|Parish')] # only study county level data
            df = pd.merge(df, df_state_abbr, left_on='state', right_on='Abbreviation', how='left',).drop(columns=['Abbreviation'])
            col = df.columns.tolist()
            col[-1] = 'state_name'
            df.columns = col
            df['state_county'] = df.state + ' ' + df.county

        except Exception as e:
            print(e)
            df = None
        finally:
            _SAIPE.__cache[year] = df

    @staticmethod
    def clear_cache():
        _SAIPE.__cache = {}


class _StatewiseEconData:
    
        __cache:dict[int, pd.DataFrame | None] = {}
        __data_dir = os.path.join(os.getcwd(), 'SASUMMARY')
    
        @staticmethod
        def get_data(year: int) -> pd.DataFrame:
            if _StatewiseEconData.__cache.get(year, None) is None:
                _StatewiseEconData._get_data(year)
            return _StatewiseEconData.__cache[year]
        
        @staticmethod
        def _get_data(year: int) -> pd.DataFrame:
            if year < 1998 or year > 2022:
                raise Exception('Data not available for this year')

            if not os.path.exists(_StatewiseEconData.__data_dir):
                _StatewiseEconData._fetch_datasource()

            file_state_pairs = os.listdir(_StatewiseEconData.__data_dir)

            file_state_pairs = [(file, file[10:12]) for file in file_state_pairs if os.path.isfile(os.path.join(_StatewiseEconData.__data_dir, file)) and file.__contains__('1998_2022') and not file.__contains__('ALL_AREAS')]

            df_state_economic = pd.DataFrame(columns=['state', 'rgdp', 'personal_income'])

            for file, state in file_state_pairs:
                offset = year - 1998 + 8
                df_temp = pd.read_csv(os.path.join(_StatewiseEconData.__data_dir, file))
                rgdp = df_temp.iloc[0, offset]
                personal_income = df_temp.iloc[4, offset]
                df_state_economic.loc[len(df_state_economic)] = [state, rgdp, personal_income]

            df_state_economic = df_state_economic[df_state_economic.state != 'US']
            df_state_economic.personal_income = df_state_economic.personal_income.astype(float)
            df_state_economic.rgdp = df_state_economic.rgdp.astype(float)
            _StatewiseEconData.__cache[year] = df_state_economic

        @staticmethod
        def _fetch_datasource():
            try:
                getHttp = requests.get(
                    f'https://apps.bea.gov/regional/zip/SASUMMARY.zip', 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
                )
                if not os.path.exists(_StatewiseEconData.__data_dir):
                    os.makedirs(_StatewiseEconData.__data_dir)
                zipfile.ZipFile(file=io.BytesIO(getHttp.content)).extractall(_StatewiseEconData.__data_dir)
                
            except Exception as e:
                print(e)
                raise
    
        @staticmethod
        def clear_cache():
            _StatewiseEconData.__cache = {}


class DataFactory:

    __call_cache:dict[(Callable, int), pd.DataFrame | None] = {}


    def cachable(func: Callable) -> pd.DataFrame:
        def wrapper(self, year:int):
            if DataFactory.__call_cache.get((func, year), None) is None:
                DataFactory.__call_cache[(func, year)] = func(self, year)
            return DataFactory.__call_cache[(func, year)]
        return wrapper


    def __init__(self, **kwargs) -> None:
        # get_state_abbr()
        self._debug = kwargs.get('debug', False)
        self.__head_start_location = _HeadStartLocation
        self.__head_start_fiscal = _HeadStartFiscal
        self.__saipe = _SAIPE
        self.__statewise_econ_data = _StatewiseEconData


    def clear_cache(self):
        self.__head_start_location.clear_cache()
        self.__head_start_fiscal.clear_cache()
        self.__saipe.clear_cache()
        self.__statewise_econ_data.clear_cache()
        self.__call_cache = {}


    @cachable
    def get_state_data(self, year: int) -> pd.DataFrame:
        df_hs_fiscal = self.__head_start_fiscal.get_data(year)
        df_state_econ = self.__statewise_econ_data.get_data(year)
        # print(df_hs_fiscal.shape)
        # print( df_state_econ.shape)
        df_data = pd.merge(df_hs_fiscal, df_state_econ, on='state', how='right')
        df_data['fund_per_child'] = np.round(df_data.federal_funding / df_data.enroll_count.astype(float), 3)
        df_data['funding_index'] = np.round(df_data.federal_funding / df_data.personal_income / df_data.enroll_count, 3)

        df_saipe = self.__saipe.get_data(year)
        df_state_child_poverty = df_saipe.groupby('state')['child_poverty_count'].sum().to_frame()
        df_state_child_poverty.reset_index(inplace=True)
        df_state_child_poverty = pd.merge(df_state_child_poverty, df_state_abbr, left_on='state',  right_on='Abbreviation', how='left').drop(columns=['Abbreviation'])
        col = df_state_child_poverty.columns.tolist()
        col[-1] = 'state_name'
        df_state_child_poverty.columns = col
        
        # print(df_state_child_poverty.shape, df_data.shape)
        df_state_child_poverty = pd.merge(
            df_state_child_poverty, df_data, on='state', how='left', suffixes=('', '_headstart')).drop(columns=['state_name_headstart']
            )
        df_state_child_poverty['enroll_rate'] = np.round(df_state_child_poverty.enroll_count.astype(float) / df_state_child_poverty.child_poverty_count.astype(float), 3)
        return df_state_child_poverty
    
    @cachable
    def get_county_data(self, year:int) -> pd.DataFrame:
        df_hs_location = self.__head_start_location.get_data()
        df_hs_location['state_county'] = df_hs_location['state'] + " " + df_hs_location['county']
        df_child_poverty = self.__saipe.get_data(year)
        
        def get_child_per_center(children:float, centers: float):
            if centers == 0 or centers == np.nan:
                return np.nan
            return round(children / centers, 3)

        def find_cpc(index):
            state_county = df_child_poverty.loc[index, 'state_county']
            count_children = df_child_poverty.loc[index, 'child_poverty_count']
            count_centers = df_hs_location[df_hs_location.state_county == state_county].shape[0]
            return get_child_per_center(count_children, count_centers)

        def check_has_center(index):
            state_county = df_child_poverty.loc[index, 'state_county']
            count_centers = df_hs_location[df_hs_location.state_county == state_county].shape[0]
            return count_centers > 0
        
        df_child_poverty['cpc'] = df_child_poverty.index.map(find_cpc)
        df_child_poverty['has_center'] = df_child_poverty.index.map(check_has_center)

        return df_child_poverty
    

data_factory = DataFactory()