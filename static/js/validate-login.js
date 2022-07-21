// проверка, авторизован ли пользователь
export function validateLogin() {
    return !!getLoginToken()
}

// получить токен авторизации
export function getLoginToken() {
    return localStorage.token
}

// выход из аккаунта
export function logOut() {
    localStorage.clear()
    location.href = '/login'
}