import java.util.*;
import java.util.stream.Collectors; 

public class conga {
	// global constants 
	public static final int RANDOM_AGENT_ID = -1;
	public static final int OPTIMIZED_AGENT_ID = 1;
	public static Square[][] board;
	public static int nodesExplored;
	public static int depth = 3;

	public static void main(String[] args) throws Exception{
		 setUpBoard();

		 Scanner scanner = new Scanner(System.in);
		 System.out.println("Press 'n' for next move");
		 while(scanner.hasNext()){
			 String s1 = scanner.next();
			 if (!s1.equals("n")){
				 break;
			 }
			board = OptimizedAgent.makeOptimizedMove(board);
			if (getNumMoves(RANDOM_AGENT_ID, board) == 0){
				System.out.println("Random Lost");
				break; 
			};

			board = RandomAgent.makeRandomMove(board);

			printBoard(board);

			if (getNumMoves(OPTIMIZED_AGENT_ID, board) == 0){
				System.out.println("Optimized Lost");
				break; 
			};
			System.out.println("Press 'n' for next move");
		 }
	} 

	public static void printBoard(Square[][] board){
		for (int i=0; i<board.length; i++){
			for (int j=0; j<board[i].length; j++){
				Square square = board[i][j];
				System.out.print(square.playerId + ":" + square.numPieces + " ");
			}	
			System.out.println("");
		}
	}

	public static void setUpBoard(){
		nodesExplored = 0;
		board = new Square[4][4];
		for (int i=0; i<board.length; i++){
			for (int j=0; j<board[i].length; j++){
				board[i][j] = new Square(0, 0);
			}
		}
		board[0][0].numPieces = 10;
		board[0][0].playerId = OPTIMIZED_AGENT_ID;
		board[3][3].numPieces = 10;
		board[3][3].playerId = RANDOM_AGENT_ID;
	}

	public static class OptimizedAgent {
		public static Square[][] makeOptimizedMove(Square[][] board) throws Exception{
			HashMap<Integer, int[]> map = new HashMap<>();
			nodesExplored = 0;
			minimax(board, 1, true, Integer.MIN_VALUE, Integer.MAX_VALUE, map);
			System.out.println("Depth explored: " + depth);
			System.out.println("Nodes explored: " + nodesExplored);
			int[] bestMove = new int[2];
			int[] bestStart = new int[2];
			int highestEval = Integer.MIN_VALUE;
			for (int key : map.keySet()){
				int[] coordinates = map.get(key);
				if (key > highestEval){
					highestEval = key;
					bestMove[0] = coordinates[2];
					bestMove[1] = coordinates[3];
					bestStart[0] = coordinates[0];
					bestStart[1] = coordinates[1];
				}
			}
			System.out.println("Optimized Agent moved: " + Arrays.toString(bestMove) + " from " + Arrays.toString(bestStart));
			return makeMove(bestMove, bestStart, OPTIMIZED_AGENT_ID, board);
		}
	}

	public static class RandomAgent {
		public static Square[][] makeRandomMove(Square[][] board) throws Exception{
			List<int[]> randomAgentSquares = getRandomAgentSquares(board);
			boolean done = false;
			List<int[]> allowedMoves = new ArrayList<>();
			int[] randomSquare = new int[2];
			while (!done){
				randomSquare = randomAgentSquares.get((int)(Math.random() * randomAgentSquares.size()));
				System.out.println(Arrays.toString(randomSquare) + " rsq");
				allowedMoves = getAllowedMoves(randomSquare, RANDOM_AGENT_ID, board);
				if (allowedMoves.size() > 0){
					done = true;
				}
			}
			int[] randomMove = allowedMoves.get((int)(Math.random() * allowedMoves.size()));
			System.out.println("Random Agent moved: " + Arrays.toString(randomMove) + " from " + Arrays.toString(randomSquare));
			return makeMove(randomMove, randomSquare, RANDOM_AGENT_ID, board);
		}
	}

	public static class Square { 
		public int playerId;
		public int numPieces;
		
		public Square(int playerId, int numPieces) {
			this.playerId = playerId; 
			this.numPieces = numPieces;
		}
	}

	public static int minimax(Square[][] board, int depth, boolean isMaximizing, int alpha, int beta, HashMap<Integer,int[]> map) throws Exception{
		// we can do this since only the optimized agent will use minimax 
		int player = isMaximizing ? OPTIMIZED_AGENT_ID : RANDOM_AGENT_ID;
		nodesExplored++;
		// depth of algorithm is capped at 3
		if (depth == 3){
			return evaluationFunction(player, board);
		}

		if (isMaximizing){
			int best = Integer.MIN_VALUE;
			for (int[] node : getOptimizedAgentSquares(board)){
				for (int[] move : getAllowedMoves(node, player, board)){
					Square[][] newBoard = makeMove(move, node, player, board);
					best = minimax(newBoard, depth+1, false, alpha, beta, map);
					if (depth == 1){
						// val : [startx, starty, movex, movey]
						map.putIfAbsent(best, new int[]{node[0], node[1], move[0], move[1]});
					}
					alpha = Math.max(alpha, best);
					if (beta <= alpha){
						break;
					}
				}
			}
			return best;
		} else {
			int best = Integer.MAX_VALUE;
			for (int[] node : getRandomAgentSquares(board)){
				for (int[] move : getAllowedMoves(node, player, board)){
					Square[][] newBoard = makeMove(move, node, player, board);
					best = minimax(newBoard, depth+1, true, alpha, beta, map);
					beta = Math.min(beta, best);
					if (beta <= alpha){
						break;
					}
				}
			}
			return best;
		}
	}

	public static Square[][] makeMove(int[] move, int[] node, int player, Square[][] board) throws Exception{
		// start by cloning input matrix
		Square[][] clone = new Square[4][4];
		for (int i=0; i<clone.length; i++){
			for (int j=0; j<clone[i].length; j++){
				clone[i][j] = new Square(0, 0);
				Square existing = board[i][j];
				Square newSquare = clone[i][j];
				newSquare.playerId = existing.playerId;
				newSquare.numPieces = existing.numPieces;
			}
		}

		Square startSquare = clone[node[0]][node[1]];
		Square firstSquare = clone[move[0]][move[1]];
		int[] dir = new int[]{move[0]-node[0], move[1]-node[1]};
		int numPieces = startSquare.numPieces;
		if (!tileAllowed(move, player, clone) || !tileAllowed(node, player, clone) || numPieces<1 || startSquare.playerId != player){
			throw new Exception(String.format("Player is not allowed to move from %s to %s, numPieces: %s, playerId: %s, newBlockId: %s", Arrays.toString(node), Arrays.toString(move), numPieces, startSquare.playerId, firstSquare.playerId));
		}

		// Checking second and third tile in direction of move
		int[] secondMove = new int[]{move[0]+dir[0], move[1]+dir[1]};
		int[] thirdMove = new int[]{secondMove[0]+dir[0], secondMove[1]+dir[1]};
		if (!tileAllowed(secondMove, player, clone)){
			// can not move further, move all to first tile
			startSquare.numPieces = 0;
			startSquare.playerId = 0;
			firstSquare.numPieces += numPieces;
			firstSquare.playerId = player;
			return clone;
		} else if (!tileAllowed(thirdMove, player, clone)){
			// can only move to second tile - one piece to first tile and rest in second
			Square secondSquare = clone[secondMove[0]][secondMove[1]];
			startSquare.numPieces = 0;
			startSquare.playerId = 0;
			firstSquare.numPieces += 1; 
			firstSquare.playerId = player;
			numPieces--;
			if (numPieces>0){
				secondSquare.numPieces += numPieces;
				secondSquare.playerId = player;
			}
		} else {
			// one piece to first, two to second and rest to third
			Square secondSquare = clone[secondMove[0]][secondMove[1]];
			Square thirdSquare = clone[thirdMove[0]][thirdMove[1]];
			startSquare.numPieces = 0;
			startSquare.playerId = 0;
			firstSquare.numPieces += 1; 
			firstSquare.playerId = player; 
			numPieces--;
			if (numPieces == 0){
				return board;
			} else if (numPieces < 3){
				secondSquare.numPieces += numPieces;
				secondSquare.playerId = player;
			} else {
				secondSquare.numPieces += 2;
				secondSquare.playerId = player;
				numPieces -= 2;
				thirdSquare.numPieces += numPieces;
				thirdSquare.playerId = player;
			}
		}

		return clone;
	}

	public static List<int[]> getOptimizedAgentSquares(Square[][] board){
		List<int[]> res = new ArrayList<>();
		for (int i=0; i<board.length; i++){
			for (int j=0; j<board[i].length; j++){
				if (board[i][j].playerId == OPTIMIZED_AGENT_ID){
					res.add(new int[]{i,j});
				}
			}
		}
		return res;
	}

	public static List<int[]> getRandomAgentSquares(Square[][] board){
		List<int[]> res = new ArrayList<>();
		for (int i=0; i<board.length; i++){
			for (int j=0; j<board[i].length; j++){
				if (board[i][j].playerId == RANDOM_AGENT_ID){
					res.add(new int[]{i,j});
				}
			}
		}
		return res;
	}

	/**
	 * goodness of a move is determined by comparing the number of moves a player can move to the 
	 * number of moves the opponent can move 
	 * 
	 * @param player
	 * @param board
	 * @return
	 */
	public static int evaluationFunction(int player, Square[][] board){
		int opponent = player == RANDOM_AGENT_ID ? OPTIMIZED_AGENT_ID : RANDOM_AGENT_ID;
		return getNumMoves(player, board) - getNumMoves(opponent, board);
	}

	/**
	 * Returns the number of moves available to the current player 
	 * 
	 * @param player
	 * @param board
	 * @return
	 */
	public static int getNumMoves(int player, Square[][] board) {
		List<int[]> currSquares = player == RANDOM_AGENT_ID ? getRandomAgentSquares(board) : getOptimizedAgentSquares(board);
		int num = 0;
		for (int[] square : currSquares){
			num += getAllowedMoves(square, player, board).size();
		}
		return num;
	}

	public static List<int[]> getAllowedMoves(int[] node, int player, Square[][] board){
		int x = node[0]; 
		int y = node[1]; 
		int[][] allMoves = new int[][]{{x+1,y}, {x,y+1}, {x+1,y+1}, {x-1,y}, {x,y-1}, {x-1,y-1}, {x+1, y-1}, {x-1,y+1}};
		return  Arrays.stream(allMoves)
				.filter(move -> tileAllowed(move, player, board))
				.collect(Collectors.toList());
	}

	public static boolean tileAllowed(int[] move, int player, Square[][] board){
		int x = move[0];
		int y = move[1];

		if (x<0 || y<0 || x>=4 || y>=4 || (board[x][y].playerId != 0 && board[x][y].playerId != player)){
			return false; 
		}
		return true;
	}
}
