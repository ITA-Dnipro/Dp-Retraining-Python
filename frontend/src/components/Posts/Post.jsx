import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import { Button } from 'react-bootstrap';
import PostIcon from './PostIcon';

const Post = () => {
    const [postInfo, setPostInfo] = useState({
        "title": "Post 1",
        "description": "Lorem ipsum dolor sit amet, ea eam saepe nemore phaedrum. Cu autem utamur nam, ex detracto adipisci pertinacia sed, te eum ceteros conceptam. Commodo dolorum iracundia nam an. Has conceptam scriptorem cu. Fugit nostro iriure cum ex, eos omittam assentior ex.",
        "goal": 100500,
        "balance": 46700
    });

    const params = useParams();

    return (
        <>
            <div className="post pt-4">
                <div className="col-4 mx-auto">
                    <div className="post-info">
                        <div className="d-flex flex-row w-100 mt-2 mb-3">
                            <div className="col-4 text-end me-2">
                                <PostIcon width="46" height="46" />
                            </div>
                            <div className="col-7 mt-auto text-start">
                                <h1>{postInfo.title}</h1>
                            </div>
                        </div>

                        <div className="d-flex flex-row w-100 my-1">
                            <div className="col-4 text-end me-2">
                                <b>Description:{' '}</b>
                            </div>
                            <div className="col-7 text-start">
                                {postInfo.description}
                            </div>
                        </div>
                        <div className="d-flex flex-row w-100 my-1">
                            <div className="col-4 text-end me-2">
                                <b>Charity:{' '}</b>
                            </div>
                            <div className="col-7 text-start">
                                Some Charity
                            </div>
                        </div>
                        <div className="d-flex flex-row w-100 my-1">
                            <div className="col-4 text-end me-2">
                                <b>Progress:{' '}</b>
                            </div>
                            <div className="col-7 text-start">
                                {postInfo.balance+" / "+postInfo.goal}
                            </div>
                        </div>
                        <Button variant="success" className="mt-3">
                              Donate
                        </Button>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Post;
