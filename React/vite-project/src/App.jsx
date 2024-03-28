import { useState } from "react";
import { TweetForm } from "./TweetForm";
import { TweetList } from "./TweetList";

const DEFAULT_TWEET = [
  {
    id : 0,
    name : "Jean",
    content : "Bonjour",
    like : 20000
  },
  {
    id : 1,
    name : "Gunther",
    content : "Guten Tag!",
    like : 8
  },
  {
    id : 2,
    name : "Pablo",
    content : "Hola",
    like : 20
  },
  {
    id : 3,
    name : "Guiseppe",
    content : "buongiorno",
    like : 51
  },
  {
    id : 4,
    name : "Peter",
    content : "Hello",
    like : 0
  },
  {
    id : 5,
    name : "Tom",
    content : "Salut",
    like : 212
  },
];

const useTweets = () => {
  const [tweets, setTweets] = useState(DEFAULT_TWEET);

  const addTweet = (tweet) => {
      
    setTweets((curr) => {
      const newTweet = {
        id: curr[curr.length - 1]?.id + 1 ?? 0,
        name : tweet.name,
        content : tweet.content,
        like : 0,
      };
  
      return [...tweets, newTweet];
    })
  }

  const onDelete = (tweetId) => {
    setTweets((curr) => curr.filter((tweet) => tweet.id !== tweetId));
  };

  const onLike = (tweetId) => {
    setTweets(curr => {
      const copyTweet = [...curr];

      const likedTweet = copyTweet.find(tweet => tweet.id === tweetId);
      likedTweet.like += 1;

      return copyTweet;
    });
  };
  return {onDelete, onLike, addTweet, tweets};
};

function App() {
  
  const {onDelete, onLike, addTweet, tweets} = useTweets();

  return (
    <div>
      <TweetForm onSubmit={addTweet} />
      <TweetList tweets={tweets} onDelete={onDelete} onLike={onLike}/>
    </div>
  );
}

export default App;