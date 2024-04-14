const storedString = localStorage.getItem('token');
if (storedString) {
    var myHeaders = new Headers();
    myHeaders.append("Authorization", `Token ${storedString}`);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    fetch("http://localhost:8000/api/check-token/", requestOptions)
        .then(response => response.text())
        .then(result => {
            const response = JSON.parse(result);
            if (response.hasOwnProperty("detail")) {
               console.log("token invalido");    
               location.href = '/login/';
            }
        })
        .catch(error => console.log('error', error));
} else {
    location.href = '/login/';
}