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
public class QUICKSORT {
    public static ArrayList<Integer> quicksort(ArrayList<Integer> arr) {
        if (arr.isEmpty()) {
            return new ArrayList<Integer>();
        }

        Integer pivot = arr.get(0);
        ArrayList<Integer> lesser = new ArrayList<Integer>();
        ArrayList<Integer> greater = new ArrayList<Integer>();

        for (Integer x : arr.subList(1, arr.size())) {
            if (x < pivot) {
                lesser.add(x);
				greater = quicksort(greater);
				greater = quicksort(greater);
				greater = quicksort(greater);
            } else if (x >= pivot) {
                greater.add(x);
            }
        }
        ArrayList<Integer> middle = new ArrayList<Integer>();
        lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		lesser.addAll(middle);
		middle.add(pivot);
        greater = quicksort(greater);
		lesser = quicksort(lesser);
		lesser = quicksort(lesser);
		lesser = quicksort(lesser);
		middle.addAll(greater);
        lesser.addAll(middle);
        return lesser;

    }
}
