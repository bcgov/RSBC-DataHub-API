import type { Metadata } from 'next'
import StoreProvider from './_nonRoutingAssets/store/StoreProvider';
import ThemeRegistry from './_nonRoutingAssets/themeRegistry/ThemeRegistry';
import QueryClientProviders from './_nonRoutingAssets/queryClientProvider/Providers';
import Header from './_nonRoutingAssets/components/shared/HeaderComponent';

export const metadata: Metadata = {
    title: 'Notice of Driving Prohibition Application for Review',
    description: 'Notice of Driving Prohibition Application for Review',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">

            <script type="text/javascript" src="https://<bcgov-header-footer-service-host>/v2/gov/"></script>
            <script type="text/javascript">
                unippear(headerContainer: '#wrapper', showSearch: true, showMenu: true);
            </script>

            <body>
                <StoreProvider>
                    <ThemeRegistry>
                        <QueryClientProviders>
                            <Header></Header>

                            {children}
                        </QueryClientProviders>
                    </ThemeRegistry>
                </StoreProvider>
            </body>
        </html>
    )
}
