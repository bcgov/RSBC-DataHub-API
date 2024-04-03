import { css } from '@emotion/react'

export const globalStyles = (theme: any) => css`
  html {
    margin: 0;
    padding: 0;
    height:100%;
  }

  /*******
   * layout.css
   *******/
  body {
    margin: 0;
    padding: 0;
    background-color: ${theme.palette.success};
  }
  
  .layout {
    width: 100%;
    display: grid;
    grid:
      "header" auto
      "main" 1fr
      "footer" auto
      / auto;
    gap: 0 8px;
  }

  .flex-item {
    display: flex;
    align-items: center;
  }

  .main { 
    grid-area: main; 
  }

  @media only screen and (max-width: 500px){
    .L {
        width: auto;
        float: none;
    }
    
    .R {
        float: none;
        width: auto;
        position: static;
    }
  }

  .mask {  
    position: fixed;
    left: 0;
    top: 0;
    z-index: 10; /* some high z-index */
    width: 100vw;
    height: 100vh;
    opacity: 0;
    user-select: none; /* prevents double clicking from highlighting entire page */
  }

  * {
    box-sizing: border-box;
  }

  /*******
   * styles.css
   *******/
  .header {
    background-color: ${theme.palette.primary.main};
    grid-area: header; 
    position: sticky;
  }

  .header-top {
    color: #fff;
    font-color: #fff;
    display: flex;
    flex-wrap: nowrap;
    height: 80px;
  }

  .header-section {
    padding: 10px 0;
    margin: 0 10px 0 0;
    height: 80px;
    max-width: 520px;
    flex-grow: 1;
    flex-shrink: 0;
    color: '#fff';
  }

  .header-info {
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    padding-top: 12px;
    padding-right: 10px;
    flex-grow: 1;
    flex-basis: 1;
    flex-shrink: 1;
    height: 70px;
  }

  main { 
    /* little formatting should be needed here */
    padding: 10px;
  }

  :focus {
    outline: 4px solid #3B99FC;
    outline-offset: 1px;
  }

  .page {
    margin-left: 25px;
    margin-right: 25px;
    margin-bottom: 25px;
  }

`;

