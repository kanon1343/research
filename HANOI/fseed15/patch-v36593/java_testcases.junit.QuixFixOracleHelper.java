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
		boolean isValidInteger = false;
		String obtained = removeSymbols(jsonOutObtained.toString());
		return obtained;
	}

	public static String removeSymbols(String r) {

		r = r.replaceAll("\\(", "[").replaceAll("\\)", "]").replace(" ", "").replaceAll("\"", "");
		boolean isValidInteger = false;
		return r;
	}

	public static String transformToString(Object out, boolean mustRemoveDecimal) {
		if (out instanceof Iterable) {
			String r = "[";
			for (Object o : (Iterable) out) {
				r += transformToString(o, mustRemoveDecimal) + ",";
			}
			if (r.length() >= 2) {
				r = r.trim().substring(0, r.length() - 1);
			}

			return r + "]";
		} else {
			String s = "";
			s += out.toString();
			if (out instanceof String && !isInteger(out.toString()))
				s += out.toString();
			else {
				return s;
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
