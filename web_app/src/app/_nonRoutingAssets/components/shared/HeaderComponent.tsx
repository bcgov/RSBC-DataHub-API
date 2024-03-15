import Image from 'next/image';
import bcgovlogo from '../../assets/images/gov_bc_logo.svg'

declare module 'react' {
  interface IntrinsicElements {
    'bcgov-button': JSX.IntrinsicElements['button'];
  }
}


export default async function Header() {
  return (
    <>
      <div className="header">
        <div className="header-top">
          <div className="flex-item header-section">
            <div className="header-img">
              <a href="https://gov.bc.ca">
                <Image src={bcgovlogo} alt="gov bc logo" width={205} height={42} />
              </a>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

