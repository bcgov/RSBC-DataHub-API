import { css } from '@emotion/react'

export const globalStyles = (theme: any) => css`
  html {
    margin: 0;
    padding: 0;
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

  .header-info img{
    border-radius: 50%;
  }
  .header-profile-button {
    // background: rgb(196 215 234 / 35%) 0% 0% no-repeat padding-box;
    border-radius: 55px;
    display: flex;
    align-items: center;
  }
  .header-text-container {
    font-weight: 700;
    margin-top: -10px;
    margin-right: 5px;
    color: #fff;
    font-size: 1rem;
    white-space: wrap;
    overflow: hidden;
    text-align: right;
  }
  .header-img-container {
    margin-left: 60px;
  }
  .header-text-agency {
    font-size: 12px;
    font-weight: 700;
    text-align: right;
    vertical-align: text-top;
    padding-left: 15px;
    padding-right: 0px;
  }
  .text-sign-out {
    color: red
  }
  .header-img {
    display: inline-block;
    padding: 2px 14px 2px 20px;
    border-right: 1px solid ${theme.palette.secondary.main}
  }

  .headerText {
    font-weight: 700;
    color: #fff;
    position:relative;
    left: 15px;
    top: 0;
    font-size: 1.375rem;
  }

  .bcrumbs-bar {
    width: fit-content;
    padding: 1px 10px 0px 10px;
    background: #bdbdbd8a 0% 0% no-repeat padding-box;
    border-radius: 10px;
    display: flex;

  }
  .bcrumbs-bar-wrapper {
    padding: 1px 1px 1px 10px;
  }

  main { 
    /* little formatting should be needed here */
    padding: 10px;
  }

  /******
   * style_header.css
   * ****/
  .headerNavContainer {
    width:100%;
    background-color: ${theme.palette.primary.main};
    border-top: 2px solid #fcba19;
  }

  .navigation-text {
    font: normal normal bold 16px/28px BC Sans;
    text-align: left;
    color: white;
    padding: 8px 20px 10px 20px;
  }
  .navigation-menu {
    background-color: #38598A;
    color: white;
    padding: 0px 20px 0px 20px;
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

  .cross-section {
    font-weight: bolder;
    font: normal normal bold 16px/22px BC Sans;
    letter-spacing: 0px;
    color: #313132;
    margin-bottom: 10px;
    margin-top: 10px;
  }

  .search-options {
    width: 75%;
    display: grid;
  }

  .search-options-fields {
      width: 100%;
      border-bottom: 1px solid #CCD6E0;
  }
  /*
    These are sample media queries only. Media queries are quite subjective
    but, in general, should be made for the three different classes of screen
    size: phone, tablet, full. 
  */

  @media screen and (min-width: 768px) {
    .navigation-menu {
      display: block;
    }
  }
`;

