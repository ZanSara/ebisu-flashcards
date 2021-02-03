import {useRouter} from "next/router";
import {FunctionComponent} from "react";
import {NextPageContext} from "next";

interface StudyProps {
    id: number
}

const Study: FunctionComponent<StudyProps> = (props) => {
    return (
        <span>Oh yes, <b>studying</b> {props.id} very hard!...</span>
    )   
}

export async function getServerSideProps(context: NextPageContext) {
    return {
        props: {
            id: context.query.id
        }, // will be passed to the page component as props
    }
}


export default Study;