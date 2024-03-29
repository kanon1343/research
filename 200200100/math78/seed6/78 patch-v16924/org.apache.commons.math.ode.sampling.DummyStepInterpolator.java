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

package org.apache.commons.math.ode.sampling;

import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;

import org.apache.commons.math.ode.DerivativeException;

/** This class is a step interpolator that does nothing.
 *
 * <p>This class is used when the {@link StepHandler "step handler"}
 * set up by the user does not need step interpolation. It does not
 * recompute the state when {@link AbstractStepInterpolator#setInterpolatedTime
 * setInterpolatedTime} is called. This implies the interpolated state
 * is always the state at the end of the current step.</p>
 *
 * @see StepHandler
 *
 * @version $Revision$ $Date$
 * @since 1.2
 */

public class DummyStepInterpolator
  extends AbstractStepInterpolator {

    /** Serializable version identifier */
    private static final long serialVersionUID = 1708010296707839488L;

  /** Simple constructor.
   * This constructor builds an instance that is not usable yet, the
   * <code>AbstractStepInterpolator.reinitialize</code> protected method
   * should be called before using the instance in order to initialize
   * the internal arrays. This constructor is used only in order to delay
   * the initialization in some cases. As an example, the {@link
   * org.apache.commons.math.ode.nonstiff.EmbeddedRungeKuttaIntegrator} uses
   * the prototyping design pattern to create the step interpolators by
   * cloning an uninitialized model and latter initializing the copy.
   */
  public DummyStepInterpolator() {
    super();
  }

  /** Simple constructor.
   * @param y reference to the integrator array holding the state at
   * the end of the step
   * @param forward integration direction indicator
   */
  public DummyStepInterpolator(final double[] y, final boolean forward) {
    super(y, forward);
  }

  /** Copy constructor.
   * @param interpolator interpolator to copy from. The copy is a deep
   * copy: its arrays are separated from the original arrays of the
   * instance
   */
  public DummyStepInterpolator(final DummyStepInterpolator interpolator) {
    super(interpolator);
  }

  /** Really copy the finalized instance.
   * @return a copy of the finalized instance
   */
  @Override
  protected StepInterpolator doCopy() {
    return new DummyStepInterpolator(this);
  }

  /** Compute the state at the interpolated time.
   * In this class, this method does nothing: the interpolated state
   * is always the state at the end of the current step.
   * @param theta normalized interpolation abscissa within the step
   * (theta is zero at the previous time step and one at the current time step)
   * @param oneMinusThetaH time gap between the interpolated time and
   * the current time
   * @throws DerivativeException this exception is propagated to the caller if the
   * underlying user function triggers one
   */
  @Override
  protected void computeInterpolatedStateAndDerivatives(final double theta, final double oneMinusThetaH)
    throws DerivativeException {
      currentState = null;
  }

  /** Write the instance to an output channel.
   * @param out output channel
   * @exception IOException if the instance cannot be written
   */
  @Override
  public void writeExternal(final ObjectOutput out)
    throws IOException {
    // save the state of the base class
    writeBaseExternal(out);
  }

  /** Read the instance from an input channel.
   * @param in input channel
   * @exception IOException if the instance cannot be read
   */
  @Override
  public void readExternal(final ObjectInput in)
    throws IOException {

    // read the base class
    final double t = readBaseExternal(in);

    // we can now set the interpolated time and state
    setInterpolatedTime(t);

  }

}
