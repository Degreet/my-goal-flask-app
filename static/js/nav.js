import { validateLogin, logOut } from './validate-login.js'

const navLinks = document.getElementById('navLinks')

if (validateLogin()) {
    navLinks.innerHTML = `
        <button class="btn btn-primary" id="logOutBtn">Выйти</button>
    `

    const logOutBtn = document.getElementById('logOutBtn')
    logOutBtn.addEventListener('click', logOut)
} else {
    navLinks.innerHTML = `
        <a class="me-3 py-2 text-dark text-decoration-none" href="/">Главная</a>
        <a href="/login"><button class="btn btn-primary">Войти</button></a>
    `
}
