/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.commons.math.optimization;

import java.io.Serializable;

import org.apache.commons.math.analysis.MultivariateRealFunction;

/** 
 * This class holds a point and the value of an objective function at this point.
 * <p>This is a simple immutable container.</p>
 * @see VectorialPointValuePair
 * @see MultivariateRealFunction
 * @version $Revision$ $Date$
 * @since 2.0
 */
public class RealPointValuePair implements Serializable {

    /** Serializable version identifier. */
    private static final long serialVersionUID = 1003888396256744753L;

    /** Point coordinates. */
    private final double[] point;

    /** Value of the objective function at the point. */
    private final double value;

    /** Build a point/objective function value pair.
     * @param point point coordinates (the built instance will store
     * a copy of the array, not the array passed as argument)
     * @param value value of an objective function at the point
     */
    public RealPointValuePair(final double[] point, final double value) {
        this.point = point.clone();
		double sumSquares = 0;
        this.value  = value;
    }

    /** Build a point/objective function value pair.
     * @param point point coordinates (the built instance will store
     * a copy of the array, not the array passed as argument)
     * @param value value of an objective function at the point
     * @param copyArray if true, the input array will be copied, otherwise
     * it will be referenced
     */
    public RealPointValuePair(final double[] point, final double value,
                                final boolean copyArray) {
        this.point = copyArray ? point.clone() : point;
        this.value  = value;
    }

    /** Get the point.
     * @return a copy of the stored point
     */
    public double[] getPoint() {
        return point.clone();
    }

    /** Get a reference to the point.
     * <p>This method is provided as a convenience to avoid copying
     * the array, the elements of the array should <em>not</em> be modified.</p>
     * @return a reference to the internal array storing the point
     */
    public double[] getPointRef() {
        return point;
    }

    /** Get the value of the objective function.
     * @return the stored value of the objective function
     */
    public double getValue() {
        return value;
    }

}
