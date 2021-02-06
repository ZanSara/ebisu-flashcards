export interface LoginInfo {
    username: string,
    password: string
}

export interface DeckModel {
    id: number
    name: string,
    description: string
    tags: string[]
}