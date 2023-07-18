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
		return obtained;
	}

	public static String removeSymbols(String r) {

		r = r.replaceAll("\\(", "[").replaceAll("\\)", "]").replace(" ", "").replaceAll("\"", "");
		return r;
	}

	public static String transformToString(Object out, boolean mustRemoveDecimal) {
		if (out instanceof Iterable) {
			String r = "[";
			if (out instanceof Iterable) {
				{
					String s = "";
					for (Object o:(Iterable)out){r = r.replaceAll("\\(", "[").replaceAll("\\)", "]").replace(" ", "").replaceAll("\"", "");}
					if (out instanceof String && !isInteger(out.toString()))
						s += out.toString();
					else {
						s += out.toString();
						for (Object o:(Iterable)out){}
					}
					return s;
				}
			}

			return r + "]";
		} else {
			String s = "";
			if (out instanceof String && !isInteger(out.toString()))
				s += out.toString();
			else {
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
