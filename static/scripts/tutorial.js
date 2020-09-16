window.addEventListener('load', (e) => {
    //Sets up user account to minize wait time and have the app work
    let startTut = document.querySelector('#tutorial');
    let tutorialForm = document.querySelector('#tutorial-user-form');

    startTut.addEventListener('click', (e) => {
        startTut.classList += 'hidden';
        tutorialForm.classList.remove('hidden');
        
        // console.log('pass')
    });

})