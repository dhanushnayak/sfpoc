import yaml
from termcolor import colored
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark import Session
from sfpro.config.Configuration import Configure
from sfpro.constants import *
from sfpro.utils import logger


class _SnowflakeSessionWrapper:
    def __init__(self):
        self._connection = None
    def get_connection(self, creds) -> Session:
        if not self._validate_connection():
            self._connection = self._create_connection(creds)
        return self._connection
    def _validate_connection(self) -> bool:
        if self._connection is None:
            return False
        if self._connection._conn._conn.is_closed():
            return False
        return True
    def _create_connection(self, creds) -> Session:
        return Session.builder.configs(creds).create()


class SessionCreated:
    def __init__(self,user) -> Session:
        self._params = Configure().get_params(user=user)
        print(self._params)

    def build(self):
        session =  None

        @st.cache_resource
        def build_session(params):
            session = Session.builder.configs(params).create()
            return session
        try:  
            session = build_session(self._params)
            print(colored("Created Session",'green'))
            logger.info(f'>>>> Session Created <<<<')
        except Exception as e:
            print(colored(e.__doc__,'red'))
            logger.error(f'>>>> Session Not Created <<<<')
        return session
    






    