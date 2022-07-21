import { validateLogin } from './validate-login.js'
if (validateLogin()) location.href = '/dashboard'