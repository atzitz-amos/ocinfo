from webq.web import request as _request


class EndpointResolver:
    def __init__(
            self,
            app,
            endpoint,
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
        self.endpoint = endpoint

        self.request = _request.Request(
            app,
            method=method,
            query=query,
            form=form,
            files=files,
            json=json,
            cookies=cookies,
            headers=headers,
            session=session
        )

    def to_response(self):
        return self.endpoint(self.request)
