import {FunctionComponent} from "react";
import {useRouter} from "next/router";

const Edit: FunctionComponent = () => {
    const router = useRouter();
    const {id} = router.query;

    return (
        <span>Oh yes, <b>editing</b> {id} very hard!...</span>
    )
}

export default Edit;