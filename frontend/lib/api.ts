export const login = async (username: string, password: string): Promise<Response> => {
    return await fetch("/api/login", {
            method: "POST",
            body: JSON.stringify({
                username: username,
                password: password
            })
        }
    );
}