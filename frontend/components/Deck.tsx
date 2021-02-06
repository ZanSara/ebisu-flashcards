import {FunctionComponent} from "react";
import {DeckModel} from "../lib/models";

import {faEdit, faList} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'

interface DeckProps {
    deck: DeckModel
}

//flex gap-2 border-t border-dashed border-gray-400 p-4 w-full

const Deck: FunctionComponent<DeckProps> = (props) => {

    return (
        <div className="flex flex-col shadow-sm rounded-xl overflow-hidden border border-gray-500">
            <main className="flex flex-col gap-4 p-4">
                <header className="flex items-center justify-between border-b border-dashed border-gray-800 pb-2">
                    <h1 className="uppercase text-2xl font-medium">{props.deck.name}</h1>
                    <div className="flex gap-4">
                        {/*
                            TODO: Add tooltips
                        */}
                        <FontAwesomeIcon icon={faList}/>
                        <FontAwesomeIcon icon={faEdit}/>
                    </div>
                </header>
                <div className="flex-grow">
                    Some content I guess
                    Some content I guess
                    Some content I guess
                    Some content I guess
                </div>
                <div className="flex flex-wrap gap-2">
                    {props.deck.tags.map(tag => <span key={tag} className="border border-dashed border-gray-800 px-4 py-1">{tag}</span>)}
                </div>
            </main>
            <a className="leading-10 text-center bg-indigo-400 text-white font-bold"
               href={`deck/${props.deck.id}/study`}>STUDY</a>
        </div>
    )
}

export default Deck;