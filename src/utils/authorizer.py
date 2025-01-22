import os
import jwt
import requets
from jwt.algorithms import RSAAlgorithm

class Auth0Authorizer:
    def __init__(self):
        self.AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
        self.AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']
        self.ALGORITHMS = ['RS256']
        self.jwks = self._get_jwks()
    
    def _get_jwks(self):
        jwks_url = f'https://{self.AUTH0_DOMAIN}/.well-known/jwks.json'
        try:
            jwks_response = requests.get(jwks_url)
             jwks_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch JWKS: {str(e)}")7
    
    def _get_public_key(self, token):
        try:
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in self.jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'n': key['n'],
                        'e': key['e']
                    }
            return rsa_key
        except Exception as e:
            raise Exception(f"Failed to get public key: {str(e)}")
        
    def verify_token(self, token):
        try:
            rsa_key = self._get_public_key(token)
            if not rsa_key:
                raise Exception('Public key not found')

            payload = jwt.decode(
                token,
                RSAAlgorithm.from_jwk(rsa_key),
                algorithms=self.ALGORITHMS,
                audience=self.AUTH0_AUDIENCE,
                issuer=f'https://{self.AUTH0_DOMAIN}/'
            )
            
            return payload
        except Exception as e:
            raise Exception(f'Token verification failed: {str(e)}')

def generate_policy(principal_id, effect, resource, context=None):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }
    
    if context:
        policy['context'] = context
    
    return policy

def auth0_verify(event, context):)
    try:
        token = event['authorizationToken']
        if not token:
            raise Exception('No authorization token provided')

        if token.lower().startswith('bearer'):
            token = token.split(' ')[1]

        auth = Auth0Authorizer()
        payload = auth.verify_token(token)

        return generate_policy(
            payload['sub'],
            'Allow',
            event['methodArn'],
            {
                'scope': payload.get('scope', ''),
                'user': payload['sub']
            }
        )

    except Exception as e:
        print(f"Authorization failed: {str(e)}")
        raise Exception('Unauthorized')