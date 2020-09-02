window.addEventListener('load', (e) => {
    console.log('hellow')

    let startTut = document.querySelector('#tutorial');
    let tutorialForm = document.querySelector('#tutorial-user-form');

    startTut.addEventListener('click', (e) => {
        startTut.classList += 'hidden';
        tutorialForm.classList.remove('hidden');
        
        console.log('pass')
    });

})