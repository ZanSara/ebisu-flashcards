import { FunctionComponent } from "react";

export interface Breadcrumb {
  name: string;
  href?: string;
}

export interface PageCardProps {
  className?: string;
  headerButtons?: JSX.Element[];
  breadcrumbs: Breadcrumb[];
}

function* generateBreadcrumbElements(breadcrumbs: Breadcrumb[]): Generator<JSX.Element> {
  if (breadcrumbs.length === 0) {
    return;
  }
  if (breadcrumbs.length > 0) {
    const breadcrumb: Breadcrumb = breadcrumbs[0];
    yield breadcrumb.href ? (
      <a key={breadcrumb.name} className="hover:underline" href={breadcrumb.href}>
        {breadcrumb.name}
      </a>
    ) : (
      <span className="text-gray-500" key={breadcrumb.name}>
        {breadcrumb.name}
      </span>
    );
  }
  if (breadcrumbs.length > 1) {
    yield (
      <span className="mx-2" key={`separator-${breadcrumbs.length}`}>
        &gt;
      </span>
    );
  }

  yield* generateBreadcrumbElements(breadcrumbs.slice(1));
}

const PageCardProps: FunctionComponent<PageCardProps> = (props) => {
  return (
    <div className={`${props.className} container md:mx-auto md:rounded-xl md:shadow overflow-hidden`}>
      <nav className="flex items-center justify-between bg-white border-b border-dashed border-gray-400 p-4">
        <div className="text-2xl font-medium ml-4">{[...generateBreadcrumbElements(props.breadcrumbs)]}</div>
        <div className="flex gap-4">{props.headerButtons}</div>
      </nav>
      {props.children}
      <footer className="w-full bg-gray-800 text-center text-gray-100 text-sm p-5">
        <span>© Ebisu Flashcards 2020. Made with ❤ and </span>
        <a className="hover:underline" href="https://nextjs.org/">
          Next.js
        </a>
        <span>.</span>
      </footer>
    </div>
  );
};

export default PageCardProps;
