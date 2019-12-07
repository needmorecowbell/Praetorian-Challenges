import requests

class RotaAPI(object):
    server = 'https://rota.praetorian.com/rota/service/play.php'
    session= None

    def __init__(self,email):
        self.session = requests.Session() # start a session to preserve cookies
        self.reset(email) # start a new game

    def _request(self, route):
        """ private request function to make calls to rota game url,
            allows for multiple attempts to retrieve a valid response
        """
        results= None
        
        # Keep attempting to make the request until there is an 
        # unhandled error, or a valid result
        while (results is None): 
            try:

                res = self.session.get(self.server + route)
                
                if(res.status_code== 200):
                    results = res.json()
            
            except Exception as e:
                print("Error: ",str(e))
                return None
            
        return results

    def place(self, loc):
        return self._request(f'?request=place&location={str(loc)}')

    def move(self, piece, loc):
        return self._request(f'?request=move&from={str(piece)}&to={str(loc)}')

    def status(self):
        return self._request("?request=status")

    def reset(self, email):
        return self._request(f'?request=new&email={email}')

    def next(self):
        return self._request("?request=next")

