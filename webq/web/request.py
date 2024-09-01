class Request:
    """ Wrapper around `flask.request` module """

    def __init__(
            self,
            app,
            method,
            query,
            form,
            files,
            json,
            cookies,
            headers,
            session
    ):
        self.app = app

        self.__r_method = method
        self.__r_query = query
        self.__r_form = form
        self.__r_files = files
        self.__r_json = json
        self.__r_cookies = cookies
        self.__r_headers = headers
        self.__r_session = session

    @property
    def method(self):
        return self.__r_method

    @property
    def query(self):
        return self.__r_query

    @property
    def form(self):
        return self.__r_form

    @property
    def files(self):
        return self.__r_files

    @property
    def json(self):
        return self.__r_json

    @property
    def cookies(self):
        return self.__r_cookies

    @property
    def headers(self):
        return self.__r_headers

    @property
    def session(self):
        return self.__r_session
