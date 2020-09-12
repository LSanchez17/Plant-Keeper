window.addEventListener('load', (e) => {

    let deleteForm = document.querySelector('#deletePlant');

    deleteForm.addEventListener('click', async (e) => {
        e.preventDefault()

        let formValue = document.querySelector('#plantId').value;
        let parentNode = document.querySelector(`plant${formValue}`);
        let response = await axios.delete(`/api/plants/delete/${formValue}`);
        console.log(response.data);
        
        parentNode.remove();
    });

})