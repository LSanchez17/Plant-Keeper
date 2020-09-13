let FORMVALUE;

const whichValueSubmits = (value) => {
    FORMVALUE = value;

    let deleteForm = document.querySelector(`#deletePlant${FORMVALUE}`);
    deleteForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        let parentNode = document.querySelector(`#plant${FORMVALUE}`);
        let response = await axios.post(`/api/plants/delete/${FORMVALUE}`);
        // alert(response.data);
        parentNode.remove();
    });
}