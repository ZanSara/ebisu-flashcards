import { FunctionComponent } from "react";

export interface PageButtonProps {
  color: string;
  onClick(): any | undefined;
}

const PushButton: FunctionComponent<PageButtonProps> = (props) => {
  const colorStyle = `bg-${props.color}-200`;

  return (
    <button
      onClick={props.onClick}
      className={`${colorStyle} py-1.5 px-4 rounded-xl hover:bg-green-300 font-medium transition-colors shadow-sm`}
    >
      {props.children}
    </button>
  );
};

export default PushButton;
