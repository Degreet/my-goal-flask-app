import { getLoginToken, validateLogin } from './validate-login.js'
if (!validateLogin()) location.href = '/login'

const createGoalForm = document.getElementById('createGoalForm')
const myGoalEl = document.getElementById('myGoal')

const goalInput = document.getElementById('goalInput')
const goalCountInput = document.getElementById('goalCountInput')

const goalTitle = document.getElementById('goalTitle')
const myGoalProgress = document.getElementById('myGoalProgress')

const upGoalBtn = document.getElementById('upGoalBtn')
const clearGoalBtn = document.getElementById('clearGoalBtn')

let goalDone, goalCount

function renderGoal() {
    // получаем результат в процентах и отображаем его
    if (goalDone < goalCount) {
        myGoalProgress.style.width = `${goalDone / goalCount * 100}%`
        myGoalProgress.classList.remove('bg-success')
        myGoalProgress.classList.add('bg-danger')
    } else {
        myGoalProgress.style.width = '100%'
        myGoalProgress.classList.remove('bg-danger')
        myGoalProgress.classList.add('bg-success')
    }

    myGoalProgress.innerText = `${goalDone}/${goalCount}` // подсказка прогресса
    myGoalEl.hidden = false // показываем пользователю его цель
}

// проверяем, есть ли у пользователя цель
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/my_goal', { // делаем запрос на сервер
            headers: { 
                'Authorization': `Bearer ${getLoginToken()}`
            }, // передаем токен авторизации
        })
    
        const result = await response.json() // получаем ответ от сервера
        if (!result.ok) return alert(result.error)
        if (!result.has) return createGoalForm.hidden = false // показываем форму создания цели

        goalTitle.innerText = result.goal
        goalDone = result.goal_done
        goalCount = result.goal_count

        renderGoal()
    } catch (e) {
        alert(e)
    }
})

// повышение кол-во выполнений
upGoalBtn.addEventListener('click', async () => {
    goalDone++
    renderGoal()

    try {
        const response = await fetch('/up_my_goal', { // делаем запрос на сервер
            headers: { 
                'Authorization': `Bearer ${getLoginToken()}`
            }, // передаем токен авторизации
        })
    
        const result = await response.json() // получаем ответ от сервера
        if (!result.ok) return alert(result.error)
    } catch (e) {
        alert(e)
    }
})

// очистка кол-во выполнений
clearGoalBtn.addEventListener('click', async () => {
    goalDone = 0
    renderGoal()
    
    try {
        const response = await fetch('/up_my_goal', { // делаем запрос на сервер
            method: 'DELETE', // с методом DELETE (чтобы очистить)
            headers: { 
                'Authorization': `Bearer ${getLoginToken()}`
            }, // передаем токен авторизации
        })
    
        const result = await response.json() // получаем ответ от сервера
        if (!result.ok) return alert(result.error)
    } catch (e) {
        alert(e)
    }
})

// создание цели
createGoalForm.addEventListener('submit', async (e) => {
    e.preventDefault()

    const goal = goalInput.value
    const goalCount = goalCountInput.value
    if (!goal || !goalCount || Number.isNaN(+goalCount)) return

    try {
        const response = await fetch('/create_my_goal', { // делаем запрос на сервер
            method: 'POST', // метод POST
            body: JSON.stringify({ goal, goal_count: +goalCount }), // передаем данные
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getLoginToken()}`
            }, // в формате JSON и передаем токен авторизации
        })
    
        const result = await response.json() // получаем ответ от сервера
        if (!result.ok) return alert(result.error)

        location.reload() // перезагружаем страницу в случае успеха
    } catch (e) {
        alert(e)
    }
})