import { useRouter } from "next/router";
import { NextPage, NextPageContext } from "next";

const EditDeckPage: NextPage = () => {
  const router = useRouter();
  const { id } = router.query;

  return (
    <div className="container max-w-2xl flex flex-col sm:my-10 sm:mx-auto sm:rounded-xl sm:shadow sm:overflow-hidden"></div>
  );
};

export async function getServerSideProps(context: NextPageContext) {
  return {
    props: {
      id: context.query.id,
    }, // will be passed to the page component as props
  };
}

export default EditDeckPage;
