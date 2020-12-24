// src/index.tsx
import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import GlobalStyle from './styles/global-styles'

ReactDOM.render(
  <BrowserRouter basename="/crawling-with-python">
    <GlobalStyle />
    <App />
  </BrowserRouter>,
  document.getElementById('root'),
)
