function Chat() {
    const { boardID } = useParams();
    const { user, setUser } = useOutletContext();
    const [board, setBoard] = useState([]);
    const [chat, setChat] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const navigate = useNavigate();
  
    function handleChangeValue(event, onSetValue) {
      onSetValue(event.target.value);
    }
  
    useEffect(() => {
      pullComments();
    }, []);
  
    async function deleteComment() {
      try {
        const response = await fetch(`/api/boards/${boardID}/comments/${commentID}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            board_id: board.boardID,
            comment: commentID,
          }),
        });
  
        if (response.ok) {
          const json = await response.json();
          navigate('/');
        } else {
          const json = await response.json()
          if(json.auth_error) {
            setUser(null)
          }
        }
      } catch (err) {
        console.error(err);
      }
    }
    
    async function pullComments(){
      try {
        const response = await fetch('/chat-history', {
          method: 'GET',
      });
      if(response.ok){
        const jsonData = await response.json();
        setChat(jsonData.comments);
      }
    } catch (error) {
      console.error('Error fetching boards:', error)
      }
    }
  
    async function handleSubmit() {
      try {
        const response = await fetch(`/api/boards/${boardID}/comments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: user,
            content: content,
          }),
        });
  
        if (response.ok) {
          const json = await response.json();
          // navigate('/');
          window.location.reload();
        } else {
          const json = await response.json()
          if(json.auth_error) {
            setUser(null)
          }
        }
      } catch (err) {
        console.error(err);
      }
    }
  
      return (
        <Flex direction={'column'} justifyContent="center" alignItems="center" height="60vh">
          <Button maxW="150px" alignSelf="center" type="submit" margin={'20px'} onClick={deleteBoard}>Delete Board</Button>
          {board && (
          <>
            <h1>{board.title}</h1>
            <p>Creator: {board.creatorID}</p>
          </>
        )}
          <Container>
    
            {comments.map(comment => (
              <Box key={comment.id} p={4} mb={4} border="1px solid #ccc" borderRadius="md">
              <p>{comment.Content}</p>
              
              <p>Creator: {comment.CreatorId}</p> 
              </Box>
            ))}
          </Container>
          <Form>
            <FormControl>
              <FormLabel>Chat</FormLabel>
              <Input type="content" onChange={e => {handleChangeValue(e, setContent);}} />
              <Button maxW="150px" alignSelf="center" type="submit" margin={'20px'} onClick={handleSubmit}>Send</Button>
            </FormControl>
        </Form>
        </Flex>
      );
    }
    
    export default Board;