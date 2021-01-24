// src/ui/main/MainContents.css.tsx
import styled from 'styled-components'
import theme from '../../styles/theme'

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;

  & > div.Buttons {
    flex: 1;
    height: 100vh;

    > div.Button {
      cursor: pointer;
      
    }
  }
`

export default Wrapper
