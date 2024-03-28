export function Tweet({id, name, content, like, onDelete, onLike, onModify}) {
    
    return (
        <div className="tweet">
            <button onClick = {() => onDelete(id)} className="delete">❌</button>
            <h3>{name}</h3>
            <p>{content}</p>
            <button onClick = {() => onLike(id)}>{like}❤️</button>
            <button onClick = {() => onModify(id)} className="modify">✏️</button>
        </div>
    );
}