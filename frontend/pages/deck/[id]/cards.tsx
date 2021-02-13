import { useRouter } from "next/router";
import { NextPage, NextPageContext } from "next";

const DeckCardsPage: NextPage = () => {
  const router = useRouter();
  const { id } = router.query;

  return (
    <span>
      Oh yes, <b>editing</b> {id} very hard!...
    </span>
  );
};

export async function getServerSideProps(context: NextPageContext) {
  return {
    props: {
      id: context.query.id,
    }, // will be passed to the page component as props
  };
}

export default DeckCardsPage;
