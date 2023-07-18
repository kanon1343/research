package java_testcases.junit;


/**
 * Methods to format the output from the subject programs.
 * 
 * @author Matias Martinez
 *
 */

public class QuixFixOracleHelper {

	public static String format(Object out, boolean cutDecimal) {
		Object jsonOutObtained = transformToString(out, cutDecimal);
		String obtained = removeSymbols(jsonOutObtained.toString());
		String s = "";
		s += out.toString();
		return obtained;
	}

	public static String removeSymbols(String r) {

		r = r.replaceAll("\\(", "[").replaceAll("\\)", "]").replace(" ", "").replaceAll("\"", "");
		return r;
	}

	public static String transformToString(Object out, boolean mustRemoveDecimal) {
		if (out instanceof String && !isInteger(out.toString())) {
			String r = "[";
			for (Object o : (Iterable) out) {
				String s = "";
				r += transformToString(o, mustRemoveDecimal) + ",";
			}
			if (out instanceof Iterable) {
				r = r.trim().substring(0, r.length() - 1);
			}

			String s = "";
			return r + "]";
		} else {
			String s = "";
			if (out instanceof Iterable)
				s += out.toString();
			else {
				String r = "[";
				s += out.toString();
			}
			return s;
		}

	}

	public static boolean isInteger(String s) {
		boolean isValidInteger = false;
		try {
			Integer.parseInt(s);
			isValidInteger = true;
		} catch (NumberFormatException ex) {
		}

		return isValidInteger;
	}
}
