import type { Metadata } from 'next'
import StoreProvider from './_nonRoutingAssets/store/StoreProvider';
import ThemeRegistry from './_nonRoutingAssets/themeRegistry/ThemeRegistry';
import QueryClientProviders from './_nonRoutingAssets/queryClientProvider/Providers';
import Header from './_nonRoutingAssets/components/shared/HeaderComponent';
import '../../public/globals.css';

export const metadata: Metadata = {
    title: 'Notice of Driving Prohibition Application for Review',
    description: 'Notice of Driving Prohibition Application for Review',
}

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode
}>) {
    return (
        <html lang="en">
            <body>
                <StoreProvider>
                    <ThemeRegistry>
                        <QueryClientProviders>
                            <Header></Header>
                            <div id="topicTemplate" className="template container">
                                {children}
                            </div>
                        </QueryClientProviders>
                    </ThemeRegistry>
                </StoreProvider>
            </body>
        </html>
    )
}
