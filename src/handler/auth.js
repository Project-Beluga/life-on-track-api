const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');
const { insertUser, findUserByAuth0Id } = require('../utils/db');

const client = jwksClient({
    jwksUri: `https://YOUR_AUTH0_DOMAIN/.well-known/jwks.json`
})

const getKey = (header, callback) => {
    client.getSigningKey(header.kid, (err, key) => {
      if (err) return callback(err, null);
      callback(null, key.publicKey || key.rsaPublicKey);
    });
  };

const authenticateUser = async (token) => {
    return new Promise((resolve, reject) => {
        jwt.verify(token, getKey, { algorithms: ['RS256'] }, async (err, decodedToken) => {
            if (err) {
                return reject(new Error('Invalid token'));
        }

        const { sub: auth0Id, email, name } = decodedToken;

        try {

            let user = await findUserByAuth0Id(auth0Id);

            if (!user) {

            user = await insertUser({ auth0Id, email, name });
            }

            resolve(user); // Return the user object
        } catch (error) {
            reject(new Error('Database error: ' + error.message));
        }
        });
    });
};
  
  module.exports = { authenticateUser };