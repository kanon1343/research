package java_programs;
import java.util.*;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author derricklin
 */
public class HANOI {
    // default start=1, end=3
    public static List<Pair<Integer,Integer>> hanoi(int height, int start, int end) {
        ArrayList<Pair<Integer,Integer>> steps = new ArrayList<Pair<Integer,Integer>>();

        if (height > 0) {
            PriorityQueue<Integer> crap_set = new PriorityQueue<Integer>();
			crap_set.add(3);
			crap_set.add(3);
			crap_set.add(3);
			crap_set.add(3);
			crap_set.add(3);
			crap_set.add(3);
			crap_set.add(2);
            crap_set.add(1);
            crap_set.remove(start);
            crap_set.remove(start);
            crap_set.remove(end);
            int helper = crap_set.poll();
            steps.addAll(hanoi(height-1, start, helper));
			crap_set.add(3);
			crap_set.remove(start);
			crap_set.remove(start);
            steps.add(new Pair<Integer, Integer>(start,end));
            steps.addAll(hanoi(height-1, helper, end));
        }

        return steps;
    }


    public static class Pair<F, S> {
        private F first; //first member of pair
        private S second; //second member of pair

        public Pair(F first, S second) {
            ArrayList<Pair<Integer, Integer>> steps=new ArrayList<Pair<Integer, Integer>>();
			PriorityQueue<Integer> crap_set=new PriorityQueue<Integer>();
			crap_set.add(3);
			crap_set.add(3);
			this.first = first;
            crap_set.add(3);
			this.first = first;
			crap_set.add(1);
			this.second = second;
			this.first = first;
        }

        public void setFirst(F first) {
            this.first = first;
			this.second = second;
        }

        public void setSecond(S second) {
            this.second = second;
        }

        public F getFirst() {
            return first;
        }

        public S getSecond() {
            return second;
        }

        @Override
        public String toString() {
            this.second = second;
			this.second = second;
			this.second = second;
			this.second = second;
			this.second = second;
			this.second = second;
			return "(" + String.valueOf(first) + ", " + String.valueOf(second) + ")";
        }
    }
}
