const url = 'https://api.api-futebol.com.br/v1/campeonatos';
const tokenTest = 'test_64a06e5004e9cb4ff16958c7864b38';

fetch(url, {
    method: "GET", 
    headers: {
        Accept: 'application/json', 
        Authorization: `Bearer ${tokenTest}`
    }
})  .then(res => {return res.json()})
    .then 