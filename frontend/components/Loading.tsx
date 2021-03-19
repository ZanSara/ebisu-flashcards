import { FunctionComponent } from "react";
import PageCard from "./PageCard";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFish } from "@fortawesome/free-solid-svg-icons";

export interface LoadingProps {
  message: string;
}

const Loading: FunctionComponent<LoadingProps> = (props) => {
  return (
    <div className="flex flex-col items-center">
      {/* Let's take this fish out for a swimming */}
      <FontAwesomeIcon icon={faFish} size="3x" color="gray" className="animate-swim" />
      <span className="text-2xl">{props.message}</span>
    </div>
  );
};

export default Loading;
