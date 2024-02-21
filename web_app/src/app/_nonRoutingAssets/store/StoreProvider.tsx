"use client";
import { useState } from "react";
import { createStore, Provider } from "jotai";
import { DevTools } from 'jotai-devtools';

const StoreProvider = ({ children }: {children: React.ReactNode}) => {
    const [store] = useState(() => createStore());
    return (
        <Provider store={store}>
            <DevTools store={store}/>
            {children}
        </Provider>
    )
}

export default StoreProvider;