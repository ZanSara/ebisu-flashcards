import Deck from '../components/Deck';
import {DeckModel} from '../lib/models';
import {FunctionComponent, useEffect} from "react";

function generateModel(id: number): DeckModel {
    const rand = Math.floor((Math.random() * 10) + 1);
    const tags: string[] = Array.from({length: rand}, () => "hello")
    
    return {
        id: id,
        name: `Deck ${id}`,
        description: `This is the description for Deck ${id}`,
        tags: tags
    }
}

// let testData: DeckModel[] = [
//     {id: 1, name: "Deck 1", description: "This is the description for Deck 1", tags: ["hello?", "hello?", "hello?", "hello?", "hello?", "hello?", "hello?"]},
//     {id: 2, name: "Deck 2", description: "This is the description for Deck 2", tags: ["hello?"]},
//     {id: 3, name: "Deck 3", description: "This is the description for Deck 3", tags: ["hello?"]},
//     {id: 4, name: "Deck 4", description: "This is the description for Deck 4", tags: ["hello?"]},
// ];

const testData: DeckModel[] = Array.from({length: 12}, (v, k) => generateModel(k));

const HomeIndex: FunctionComponent = () => {
    useEffect(() => {
        document.querySelector("body")?.classList.add("bg-indigo-200")
    });

    return (
        <div className="container flex flex-col sm:my-10 sm:mx-auto sm:rounded-xl sm:shadow sm:overflow-hidden">
            <nav
                className="flex justify-between bg-white border-b border-dashed border-gray-400 w-full p-4">
                <h1 className="uppercase text-2xl font-medium ml-4 mt-auto mb-auto">Home</h1>
                <div className="flex gap-4">
                    <a className="py-1 px-2 rounded-xl border-4 border-green-400" href="deck/new">New deck</a>
                    <a className="py-1 px-2 rounded-xl border-4 border-red-400" href="logout">Logout</a>
                </div>
            </nav>
            <main className="grid items-start lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-1 auto-rows-max gap-8 p-8 bg-white">
                {testData.map(
                    deckModel => <Deck key={deckModel.id} deck={deckModel}/>
                )}
            </main>
            <footer className="w-full bg-gray-800 text-center">
                    <span className="inline-block text-gray-100 text-sm p-5">
                        © Ebisu Flashcards 2020. Made with ❤ and <a className="hover:underline"
                                                                    href="https://nextjs.org/">Next.js</a>.
                    </span>
            </footer>
        </div>
    )
}

export default HomeIndex;
