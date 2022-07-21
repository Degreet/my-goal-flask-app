const loginForm = document.getElementById('loginForm')
const loginInput = document.getElementById('login')
const passwordInput = document.getElementById('password')
const alertEl = document.getElementById('alert')

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault() // отменяем перезагрузку страницы 

    const login = loginInput.value // получаем логин
    const password = passwordInput.value // получаем пароль
    if (!login || password.length < 8) return // проверяем данные

    try {
        const response = await fetch('/login', { // делаем запрос на сервер
            method: 'POST', // метод POST
            body: JSON.stringify({ login, password }), // передаем данные
            headers: { 'Content-Type': 'application/json' }, // в формате JSON
        })
    
        const result = await response.json() // получаем ответ от сервера
        
        if (!result.ok) { // показываем ошибку
            alertEl.innerText = result.error
            alertEl.hidden = false
            return
        }

        localStorage.token = result.token // сохраняем токен
        location.href = '/dashboard' // отправляем в главный кабинет
    } catch (e) {
        console.error(e.error)
    }
})
